from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from authlib.integrations.starlette_client import OAuth
from functools import wraps

class OAuth2Auth:
    def __init__(self, app: FastAPI, provider="google", client_id=None, client_secret=None):
        self.oauth = OAuth()
        self.oauth.register(
            name=provider,
            client_id=client_id or "default_client_id",
            client_secret=client_secret or "default_client_secret",
            access_token_url=f'https://{provider}.com/oauth/token',
            authorize_url=f'https://{provider}.com/oauth/authorize',
            client_kwargs={"scope": "openid email profile"},
        )
        self.app = app

    def login_required(self, f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            token = kwargs.get("token") or Request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Missing token")
            # Logic to check token with OAuth2 provider can be added here
            return await f(*args, **kwargs)
        return decorated_function

# Example usage of the class in a FastAPI app
app = FastAPI()

oauth2_auth = OAuth2Auth(app)

# Sample protected route (you can define your own routes as needed)
@app.get("/protected")
@oauth2_auth.login_required
async def protected_route(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return {"message": "This is a protected route"}
