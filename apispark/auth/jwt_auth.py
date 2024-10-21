import jwt
from functools import wraps
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

class JWTAuth:
    def __init__(self, secret="default_secret", algorithm="HS256", authorizationUrl=None, tokenUrl=None):
        self.secret = secret
        self.algorithm = algorithm
        self.authorizationUrl = authorizationUrl
        self.tokenUrl = tokenUrl

    def decode_token(self, token):
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None

    def jwt_required(self, token: str = Depends(OAuth2AuthorizationCodeBearer(authorizationUrl="your_authorization_url", tokenUrl="your_token_url"))):
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        token_data = self.decode_token(token)
        if not token_data:
            raise HTTPException(status_code=403, detail="Invalid token")
        return token_data
