
import pytest
from fastapi.testclient import TestClient
import ccxt
from mcp.app import app

client = TestClient(app)

class DummyEx:
    def __init__(self, *args, **kwargs):
        self.markets = {'BTC/USDT': {}}
    def fetch_ticker(self, symbol):
        if symbol == 'ERR': raise Exception('fail')
        return {'symbol': symbol, 'timestamp': 123, 'datetime': '2025-01-01T00:00:00Z', 'bid': 100, 'ask': 101, 'last': 100.5, 'info': {}}
    def fetch_ohlcv(self, symbol, since=None, limit=None, params=None):
        # return sample data 200 rows
        return [[i,1,2,0.5,1.5,10] for i in range(200)]
    def load_markets(self):
        return self.markets

@pytest.fixture(autouse=True)
def stub_ccxt(monkeypatch):
    monkeypatch.setattr(ccxt, 'exchanges', ['dummyex'])
    monkeypatch.setattr(ccxt, 'dummyex', DummyEx)
    yield

def test_health():
    r = client.get('/health')
    assert r.status_code == 200 and r.json()=={'status':'ok'}

def test_ticker_ok():
    r = client.get('/ticker?exchange=dummyex&symbol=BTC/USDT', headers={'X-API-KEY':'demo-key-123'})
    assert r.status_code == 200
    j = r.json()
    assert j['symbol']=='BTC/USDT'

def test_historical_pagination():
    r = client.get('/historical?exchange=dummyex&symbol=BTC/USDT&limit=10&page=2', headers={'X-API-KEY':'demo-key-123'})
    assert r.status_code == 200
    j = r.json()
    assert j['page']==2 and len(j['ohlcv'])==10

def test_markets():
    r = client.get('/markets?exchange=dummyex', headers={'X-API-KEY':'demo-key-123'})
    assert r.status_code==200
    assert 'markets' in r.json()
