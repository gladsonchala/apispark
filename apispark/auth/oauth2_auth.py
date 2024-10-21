from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from authlib.integrations.starlette_client import OAuth
from functools import wraps

class OAuth2Auth:
    def __init__(self, app: FastAPI, provider, client_id, client_secret, authorize_url, access_token_url, client_kwargs):
        self.oauth = OAuth()
        self.oauth.register(
            name=provider,
            client_id=client_id,
            client_secret=client_secret,
            access_token_url=access_token_url,
            authorize_url=authorize_url,
            client_kwargs=client_kwargs,
        )
        self.app = app

    def login_required(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        # Logic to check token with OAuth2 provider can be added here
        return token
