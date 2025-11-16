
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Any, Dict, List
import asyncio, traceback, logging
from .models import TickerResponse, HistoricalResponse
from .adapters import get_exchange, ensure_ohlcv
from .cache import TICKER_CACHE, HIST_CACHE
from cachetools import cached
from .config import settings
from .auth import api_key_auth
from .retries import retry_on_exception
from .metrics import metrics_response
from .middleware import logging_middleware
from prometheus_client import Counter
from tenacity import retry, stop_after_attempt, wait_exponential

app = FastAPI(title='MCP Server - Option B')

# register middleware
app.middleware('http')(logging_middleware)

logger = logging.getLogger('mcp')
logging.basicConfig(level=logging.INFO)

@app.get('/health')
async def health():
    return {'status':'ok'}

# metrics endpoint
@app.get('/metrics')
async def metrics():
    return metrics_response()

# Cached fetchers (sync functions run in threadpool)
@cached(TICKER_CACHE)
@retry_on_exception()
def _fetch_ticker_sync(exchange_id: str, symbol: str) -> dict:
    ex = get_exchange(exchange_id)
    return ex.fetch_ticker(symbol)

@app.get('/ticker', response_model=TickerResponse, tags=['market'])
async def ticker(exchange: str = Query(..., description='Exchange id (ccxt)'), symbol: str = Query(..., description='Symbol like BTC/USDT'), api_key: str = Depends(api_key_auth)):
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, _fetch_ticker_sync, exchange, symbol)
        return {
            'exchange': exchange,
            'symbol': symbol,
            'timestamp': data.get('timestamp'),
            'datetime': data.get('datetime'),
            'bid': data.get('bid'),
            'ask': data.get('ask'),
            'last': data.get('last'),
            'info': data.get('info'),
        }
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=502, detail=f'Failed to fetch ticker: {e}')

@cached(HIST_CACHE)
@retry_on_exception()
def _fetch_ohlcv_sync(exchange_id: str, symbol: str, since: Optional[int], limit: int):
    ex = get_exchange(exchange_id)
    ensure_ohlcv(ex)
    # fetch full data and return; pagination is applied at API layer
    return ex.fetch_ohlcv(symbol, since=since, limit=limit*5 if limit else None, params={})

@app.get('/historical', response_model=HistoricalResponse, tags=['market'])
async def historical(exchange: str = Query(...), symbol: str = Query(...), since: Optional[int] = Query(None), limit: int = Query(100, ge=1, le=1000), page: int = Query(1, ge=1), api_key: str = Depends(api_key_auth)):
    try:
        loop = asyncio.get_event_loop()
        # we'll fetch limit * page_size to allow pagination, then slice
        data = await loop.run_in_executor(None, _fetch_ohlcv_sync, exchange, symbol, since, limit)
        # pagination: page starts at 1
        start = (page - 1) * limit
        end = start + limit
        sliced = data[start:end] if isinstance(data, list) else data
        return {'exchange': exchange, 'symbol': symbol, 'ohlcv': sliced, 'page': page, 'limit': limit}
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=502, detail=f'Failed to fetch historical: {e}')

@app.get('/markets', tags=['market'])
async def markets(exchange: str = Query(...), api_key: str = Depends(api_key_auth)):
    try:
        ex = get_exchange(exchange)
        markets = ex.load_markets()
        return {'exchange': exchange, 'markets': list(markets.keys())}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=502, detail=str(e))

# WebSocket manager and pollers (query params)
class WSManager:
    def __init__(self):
        self._clients: Dict[str, list] = {}
        self._tasks: Dict[str, asyncio.Task] = {}
        self._lock = asyncio.Lock()

    async def connect(self, key: str, ws: WebSocket):
        await ws.accept()
        async with self._lock:
            self._clients.setdefault(key, []).append(ws)
            if key not in self._tasks:
                self._tasks[key] = asyncio.create_task(self._poller(key))

    def disconnect(self, key: str, ws: WebSocket):
        clients = self._clients.get(key, [])
        if ws in clients:
            clients.remove(ws)
        if not clients and key in self._tasks:
            self._tasks[key].cancel()
            del self._tasks[key]
            del self._clients[key]

    async def _poller(self, key: str):
        exchange_id, symbol = key.split("::", 1)
        try:
            while True:
                try:
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, _fetch_ticker_sync, exchange_id, symbol)
                except Exception as e:
                    data = {'error': str(e)}
                await self._broadcast(key, {'type':'ticker','data':data})
                await asyncio.sleep(settings.poll_interval)
        except asyncio.CancelledError:
            return

    async def _broadcast(self, key: str, message: dict):
        for ws in list(self._clients.get(key, [])):
            try:
                await ws.send_json(message)
            except:
                pass

manager = WSManager()

@app.websocket('/ws')
async def ws_ticker(ws: WebSocket, exchange: str = Query(...), symbol: str = Query(...)):
    key = f"{exchange}::{symbol}"
    await manager.connect(key, ws)
    try:
        while True:
            # receive to keep the socket alive
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(key, ws)
    except Exception:
        manager.disconnect(key, ws)
        try:
            await ws.close()
        except:
            pass
