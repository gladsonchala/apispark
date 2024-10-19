from.api_key_auth import APIKeyAuth
from.basic_auth import BasicAuth
from.jwt_auth import JWTAuth
from.oauth2_auth import OAuth2Auth

class Auth:
    def __init__(self, security=None, **kwargs):
        self.security = security
        if security == "jwt":
            self.jwt_auth = JWTAuth(**kwargs)
            self.jwt_required = self.jwt_auth.jwt_required
        elif security == "oauth2":
            self.oauth2_auth = OAuth2Auth(**kwargs)
            self.login_required = self.oauth2_auth.login_required
        elif security == "apikey":
            self.apikey_auth = APIKeyAuth(**kwargs)
            self.api_key_required = self.apikey_auth.api_key_required
        elif security == "basic":
            self.basic_auth = BasicAuth(**kwargs)
            self.basic_auth_required = self.basic_auth.basic_auth_required
