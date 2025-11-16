
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import ccxt

# Retry decorator for exchange calls
def retry_on_exception():
    return retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=5))
