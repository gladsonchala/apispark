from fastapi import HTTPException, Header
from functools import wraps
import base64

class BasicAuth:
    def __init__(self, valid_users):
        self.valid_users = valid_users

    def basic_auth_required(self, auth: str = Header(None)):
        if not auth:
            raise HTTPException(status_code=401, detail="Missing credentials")
        try:
            auth_type, creds = auth.split()
            if auth_type.lower() != "basic":
                raise HTTPException(status_code=403, detail="Invalid auth type")
            decoded_creds = base64.b64decode(creds).decode("utf-8")
            username, password = decoded_creds.split(":")
            if username not in self.valid_users or self.valid_users[username] != password:
                raise HTTPException(status_code=403, detail="Invalid credentials")
        except Exception:
            raise HTTPException(status_code=403, detail="Invalid credentials format")
        return auth
