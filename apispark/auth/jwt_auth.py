from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class JWTAuth:
    def __init__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int = 30):
        """
        Initialize an instance of JWTAuth.

        Args:
            secret_key (str): Secret key used to encode and decode the JWT.
            algorithm (str): Algorithm used to encode and decode the JWT. Should be one of the algorithms supported by the `jose` library.
            access_token_expire_minutes (int, optional): The number of minutes the JWT will be valid after it is issued. Defaults to 30.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """
        Create an access token that can be used to authenticate with the API.

        Args:
            data (dict): Data to be included in the access token.
            expires_delta (timedelta, optional): The amount of time the access token will be valid after it is issued. Defaults to None.

        Returns:
            str: The encoded access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str):
        """
        Verify that the given token is valid and return the payload.

        Args:
            token (str): The token to be verified.

        Returns:
            dict: The payload of the token.

        Raises:
            HTTPException: If the token is invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )

    def jwt_required(self, token: str = Depends(oauth2_scheme)):
        """
        Decorator to check if the JWT token is valid.

        Args:
            token (str): The JWT token passed in the Authorization header.

        Returns:
            dict: The payload of the JWT token.

        Raises:
            HTTPException: If the JWT token is invalid.
        """
        payload = self.verify_token(token)
        return payload
