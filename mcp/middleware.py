
import time, logging
from fastapi import Request
from .metrics import REQUEST_COUNT, REQUEST_LATENCY
from .ratelimit import check_rate_limit

logger = logging.getLogger('mcp')

async def logging_middleware(request: Request, call_next):
    start = time.time()
    try:
        # rate limit check
        try:
            check_rate_limit(request)
        except Exception as e:
            raise e
        response = await call_next(request)
        return response
    finally:
        elapsed = time.time() - start
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(elapsed)
        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=str(getattr(response, 'status_code', '500'))).inc()
        logger.info(f"{request.method} {request.url.path} completed in {elapsed:.3f}s") 
