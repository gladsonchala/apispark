import jwt
from functools import wraps
from fastapi import Request, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

class JWTAuth:
    def __init__(self, secret="default_secret", algorithm="HS256"):
        self.secret = secret
        self.algorithm = algorithm
        self.oauth2_scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl="your_authorization_url",  # Replace with your actual authorization URL
            tokenUrl="your_token_url"                   # Replace with your actual token URL
        )

    def decode_token(self, token):
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None

    def jwt_required(self, f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            token = await self.oauth2_scheme(request)
            if not token:
                raise HTTPException(status_code=401, detail="Missing token")
            token_data = self.decode_token(token)
            if not token_data:
                raise HTTPException(status_code=403, detail="Invalid token")
            return await f(request, *args, **kwargs)
        return decorated_function
