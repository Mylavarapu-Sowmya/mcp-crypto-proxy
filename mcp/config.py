
import yaml, os
from pydantic import BaseSettings

class Settings(BaseSettings):
    poll_interval: int = 2
    ticker_cache_ttl: int = 5
    historical_cache_ttl: int = 60
    rate_limit_per_minute: int = 60
    api_keys: list = ["demo-key-123"]

cfg_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
try:
    with open(cfg_path, "r") as f:
        data = yaml.safe_load(f) or {}
except FileNotFoundError:
    data = {}
settings = Settings(**data)
