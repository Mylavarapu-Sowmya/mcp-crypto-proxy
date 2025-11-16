
import ccxt
from typing import Any
from .exceptions import ExchangeNotSupported, ExchangeCapabilityError
from cachetools import LRUCache, cached
import threading

_EX_CACHE = LRUCache(maxsize=50)

@cached(_EX_CACHE)
def get_exchange(exchange_id: str) -> Any:
    if exchange_id not in ccxt.exchanges:
        raise ExchangeNotSupported(exchange_id)
    ex_class = getattr(ccxt, exchange_id)
    ex = ex_class({'enableRateLimit': True})
    return ex

def ensure_ohlcv(exchange):
    if not hasattr(exchange, "fetch_ohlcv"):
        raise ExchangeCapabilityError("Exchange does not support OHLCV (historical) data")
