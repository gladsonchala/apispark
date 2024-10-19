from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .auth.jwt_auth import JWTAuth
from .auth.oauth2_auth import OAuth2Auth
from .auth.api_key_auth import APIKeyAuth
from .auth.basic_auth import BasicAuth

from .routers.router import Router
from .middleware import MiddlewareManager
from .exceptions.exception_handler import custom_exception_handler, http_exception_handler

class ApiSparkApp:
    def __init__(self, module_globals, security=None, **kwargs):
        self.app = FastAPI()
        self.router = Router()
        self.middleware_manager = MiddlewareManager()

        self.router.register_routes(module_globals)
        self.middleware_manager.register_middlewares(self.app)
        self._add_health_check()
        self._register_exception_handlers()

        self.security_method = None
        self._init_security(security, kwargs)

    def _init_security(self, security, kwargs):
        # Initialize security methods
        if security == "jwt":
            self.security_method = JWTAuth(
                secret=kwargs.get("secret", "default_jwt_secret"),
                algorithm=kwargs.get("algorithm", "HS256")
            )
        elif security == "oauth2":
            self.security_method = OAuth2Auth(
                app=self.app,
                provider=kwargs.get("provider", "google"),
                client_id=kwargs.get("client_id", "default_client_id"),
                client_secret=kwargs.get("client_secret", "default_client_secret")
            )
        elif security == "apikey":
            self.security_method = APIKeyAuth(
                valid_keys=kwargs.get("valid_keys", ["default_key"])
            )
        elif security == "basic":
            self.security_method = BasicAuth(
                valid_users=kwargs.get("valid_users", {"admin": "password"})
            )

    def include_router(self):
        self.router.include_in_app(self.app)

    def get_app(self):
        self.include_router()
        return self.app

    def _add_health_check(self):
        @self.app.get("/health", tags=["Health"])
        async def health_check():
            return JSONResponse(content={"status": "healthy", "message": "API is running properly."})

    def _register_exception_handlers(self):
        self.app.add_exception_handler(Exception, custom_exception_handler)
        self.app.add_exception_handler(HTTPException, http_exception_handler)

    def add_cors(self, allow_origins=["*"], allow_methods=["GET", "POST"]):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=allow_methods,
            allow_headers=["*"],
        )

    def serve_static(self, path, directory):
        self.app.mount(path, StaticFiles(directory=directory), name="static")

    def route(self, path, methods=["GET"], protected=False):
        def decorator(func):
            dependencies = []
            if protected and self.security_method:
                dependencies = self._get_dependencies_for_route()

            self.router.router.add_api_route(path, func, methods=methods, dependencies=dependencies)
            return func

        return decorator

    def _get_dependencies_for_route(self):
        # Get dependencies based on the security method
        if isinstance(self.security_method, JWTAuth):
            return [Depends(self.security_method.jwt_required)]
        elif isinstance(self.security_method, OAuth2Auth):
            return [Depends(self.security_method.login_required)]
        elif isinstance(self.security_method, APIKeyAuth):
            return [Depends(self.security_method.api_key_required)]
        elif isinstance(self.security_method, BasicAuth):
            return [Depends(self.security_method.basic_auth_required)]
        return []
