
from cachetools import TTLCache
from .config import settings

TICKER_CACHE = TTLCache(maxsize=2000, ttl=settings.ticker_cache_ttl)
HIST_CACHE = TTLCache(maxsize=1000, ttl=settings.historical_cache_ttl)
