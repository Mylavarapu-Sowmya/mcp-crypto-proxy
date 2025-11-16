
from fastapi import Header, HTTPException, Depends
from .config import settings

def api_key_auth(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key not in settings.api_keys:
        raise HTTPException(status_code=401, detail='Invalid or missing API key')
    return x_api_key
