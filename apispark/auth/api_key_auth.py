from functools import wraps
from fastapi import HTTPException, Header

class APIKeyAuth:
    def __init__(self, valid_keys=["default_key"]):
        self.valid_keys = valid_keys

    def api_key_required(self, api_key: str = Header(None)):
        if api_key not in self.valid_keys:
            raise HTTPException(status_code=403, detail="Invalid API Key")
        return api_key
