from jose import JWTError, jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

class JWTAuth:
    def __init__(self, secret, algorithm, authorizationUrl=None, tokenUrl=None):
        self.secret = secret
        self.algorithm = algorithm
        self.authorizationUrl = authorizationUrl
        self.tokenUrl = tokenUrl
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.tokenUrl)

    def jwt_required(self, token: str = Depends(lambda: self.oauth2_scheme)):
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        token_data = self.decode_token(token)
        if not token_data:
            raise HTTPException(status_code=403, detail="Invalid token")
        return token_data

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt
