
from pydantic import BaseModel
from typing import Optional, Any, List

class TickerResponse(BaseModel):
    exchange: str
    symbol: str
    timestamp: Optional[int]
    datetime: Optional[str]
    bid: Optional[float]
    ask: Optional[float]
    last: Optional[float]
    info: Optional[dict]

class HistoricalResponse(BaseModel):
    exchange: str
    symbol: str
    ohlcv: List[List[Any]]
    page: Optional[int] = None
    limit: Optional[int] = None

class ErrorResponse(BaseModel):
    detail: str
