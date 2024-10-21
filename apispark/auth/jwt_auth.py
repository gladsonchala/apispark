import jwt
from functools import wraps
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

class JWTAuth:
    def __init__(self, secret, authorizationUrl=None, tokenUrl=None):
        self.secret = secret
        self.authorizationUrl = authorizationUrl
        self.tokenUrl = tokenUrl
        self.oauth2_scheme = OAuth2AuthorizationCodeBearer(authorization_url=self.authorizationUrl, token_url=self.tokenUrl)

    def jwt_required(self, token: str = Depends(lambda: self.oauth2_scheme)):
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        token_data = self.decode_token(token)
        if not token_data:
            raise HTTPException(status_code=403, detail="Invalid token")
        return token_data

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
