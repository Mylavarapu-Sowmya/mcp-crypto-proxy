
from fastapi import HTTPException

class ExchangeNotSupported(HTTPException):
    def __init__(self, exchange: str):
        super().__init__(status_code=400, detail=f"Unknown or unsupported exchange: {exchange}")

class ExchangeCapabilityError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=400, detail=msg)

class RateLimitExceeded(HTTPException):
    def __init__(self):
        super().__init__(status_code=429, detail='Rate limit exceeded')
