
import time, threading
from .config import settings
from .exceptions import RateLimitExceeded
from fastapi import Request

# Simple in-memory token bucket per IP
_lock = threading.Lock()
_buckets = {}  # ip -> (tokens, last_timestamp)

def _get_key(request: Request):
    client = request.client.host if request.client else 'unknown'
    return client

def check_rate_limit(request: Request):
    key = _get_key(request)
    now = time.time()
    with _lock:
        tokens, last = _buckets.get(key, (settings.rate_limit_per_minute, now))
        # refill
        elapsed = now - last
        rate_per_sec = settings.rate_limit_per_minute / 60.0
        tokens = min(settings.rate_limit_per_minute, tokens + elapsed * rate_per_sec)
        if tokens < 1:
            _buckets[key] = (tokens, now)
            raise RateLimitExceeded()
        # consume one token
        tokens -= 1
        _buckets[key] = (tokens, now)
