from fastapi import Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, APIKeyHeader
from .api_key_auth import APIKeyAuth
from .basic_auth import BasicAuth
from .jwt_auth import JWTAuth
from .oauth2_auth import OAuth2Auth

class Auth:
    def __init__(self, security=None, **kwargs):
        self.security = security
        if security == "jwt":
            self.jwt_auth = JWTAuth(
                secret=kwargs.get("secret"),
                algorithm=kwargs.get("algorithm"),
                authorizationUrl=kwargs.get("authorizationUrl"),
                tokenUrl=kwargs.get("tokenUrl")
            )
            self.jwt_required = self.jwt_auth.jwt_required
        elif security == "oauth2":
            self.oauth2_auth = OAuth2Auth(
                app=kwargs.get("app"),
                provider=kwargs.get("provider"),
                client_id=kwargs.get("client_id"),
                client_secret=kwargs.get("client_secret")
            )
            self.login_required = self.oauth2_auth.login_required
        elif security == "apikey":
            self.apikey_auth = APIKeyAuth(valid_keys=kwargs.get("valid_keys"))
            self.api_key_required = self.apikey_auth.api_key_required
        elif security == "basic":
            self.basic_auth = BasicAuth(valid_users=kwargs.get("valid_users"))
            self.basic_auth_required = self.basic_auth_required

    def basic_auth_required(self, credentials: HTTPBasicCredentials = Security(HTTPBasic())):
        return self.basic_auth.basic_auth_required(credentials)
