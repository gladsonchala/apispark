# File: /apispark/auth/__init__.py

from fastapi import Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, APIKeyHeader
from .api_key_auth import APIKeyAuth
from .basic_auth import BasicAuth
from .oauth2_auth import OAuth2Auth
from .jwt_auth import JWTAuth

class Auth:
    def __init__(self, security=None, **kwargs):
        """
        Initializes the Auth class with the specified security method.

        Args:
            security (str, optional): The type of security to use. Options are "oauth2", "apikey", "basic", or "jwt".
            **kwargs: Additional keyword arguments specific to the chosen security method.

        Attributes:
            security (str): The type of security method being used.
            oauth2_auth (OAuth2Auth, optional): Instance managing OAuth2 authentication, if specified.
            login_required (callable, optional): Function to enforce login for OAuth2 authentication.
            apikey_auth (APIKeyAuth, optional): Instance managing API Key authentication, if specified.
            api_key_required (callable, optional): Function to enforce API Key authentication.
            basic_auth (BasicAuth, optional): Instance managing Basic authentication, if specified.
            basic_auth_required (callable, optional): Function to enforce Basic authentication.
            jwt_auth (JWTAuth, optional): Instance managing JWT authentication, if specified.
            jwt_required (callable, optional): Function to enforce JWT authentication.
        """
        self.security = security
        if security == "oauth2":
            self.oauth2_auth = OAuth2Auth(
                app=kwargs.get("app"),
                provider=kwargs.get("provider"),
                client_id=kwargs.get("client_id"),
                client_secret=kwargs.get("client_secret"),
                authorize_url=kwargs.get("authorize_url"),
                access_token_url=kwargs.get("access_token_url"),
                client_kwargs=kwargs.get("client_kwargs", {"scope": "openid email profile"})
            )
            self.login_required = self.oauth2_auth.login_required
        elif security == "apikey":
            self.apikey_auth = APIKeyAuth(valid_keys=kwargs.get("valid_keys"))
            self.api_key_required = self.apikey_auth.api_key_required
        elif security == "basic":
            self.basic_auth = BasicAuth(valid_users=kwargs.get("valid_users"))
            self.basic_auth_required = self.basic_auth_required
        elif security == "jwt":
            self.jwt_auth = JWTAuth(
                secret_key=kwargs.get("secret"),
                algorithm=kwargs.get("algorithm"),
                access_token_expire_minutes=kwargs.get("access_token_expire_minutes", 30)
            )
            self.jwt_required = self.jwt_auth.jwt_required

    def basic_auth_required(self, credentials: HTTPBasicCredentials = Security(HTTPBasic())):
        """
        Enforces basic authentication for an endpoint.

        This method uses HTTP Basic authentication to verify the provided
        credentials against a list of valid users. If the credentials
        are invalid, an HTTPException with a 401 status code is raised.

        Args:
            credentials (HTTPBasicCredentials, optional): The credentials provided
            by the client. Defaults to using FastAPI's Security dependency with
            HTTPBasic.

        Returns:
            HTTPBasicCredentials: The validated credentials if authentication is successful.
        """
        return self.basic_auth.basic_auth_required(credentials)
