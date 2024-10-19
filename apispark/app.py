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
    """
    This class provides a convenient wrapper for creating FastAPI applications
    and auto-registering routes based on naming conventions.
    """
    def __init__(self, module_globals, security=None, **kwargs):
        self.app = FastAPI()
        self.router = Router()
        self.middleware_manager = MiddlewareManager()  # Middleware manager instance

        self.router.register_routes(module_globals)
        self.middleware_manager.register_middlewares(self.app)  # Register middleware
        self._add_health_check()

        # Register custom exception handlers
        self._register_exception_handlers()

        self.security_method = None

        # JWT Authentication
        if security == "jwt":
            self.security_method = JWTAuth(
                secret=kwargs.get("secret", "default_jwt_secret"),
                algorithm=kwargs.get("algorithm", "HS256")
            )

        # OAuth2 Authentication
        elif security == "oauth2":
            self.security_method = OAuth2Auth(
                app=self.app,
                provider=kwargs.get("provider", "google"),
                client_id=kwargs.get("client_id", "default_client_id"),
                client_secret=kwargs.get("client_secret", "default_client_secret")
            )

        # API Key Authentication
        elif security == "apikey":
            self.security_method = APIKeyAuth(
                valid_keys=kwargs.get("valid_keys", ["default_key"])
            )

        # Basic Authentication
        elif security == "basic":
            self.security_method = BasicAuth(
                valid_users=kwargs.get("valid_users", {"admin": "password"})
            )

    def include_router(self):
        """
        Include the router with all automatically registered routes into the app.
        """
        self.router.include_in_app(self.app)

    def get_app(self):
        """
        Return the FastAPI app instance after including all routes.
        """
        self.include_router()
        return self.app

    def _add_health_check(self):
        """
        Add a default health check endpoint to the FastAPI app.
        This allows users to verify that the application is running correctly.
        """
        @self.app.get("/health", tags=["Health"])
        async def health_check():
            return JSONResponse(content={"status": "healthy", "message": "API is running properly."})

    def _register_exception_handlers(self):
        """
        Register the custom exception handlers.
        """
        self.app.add_exception_handler(Exception, custom_exception_handler)
        self.app.add_exception_handler(HTTPException, http_exception_handler)

    def add_background_task(self, task, *args, **kwargs):
        background_tasks = BackgroundTasks()
        background_tasks.add_task(task, *args, **kwargs)
        return background_tasks

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
            if protected and self.security_method:
                if isinstance(self.security_method, JWTAuth):
                    dependencies = [Depends(self.security_method.jwt_required)]
                elif isinstance(self.security_method, OAuth2Auth):
                    dependencies = [Depends(self.security_method.login_required)]
                elif isinstance(self.security_method, APIKeyAuth):
                    dependencies = [Depends(self.security_method.api_key_required)]
                elif isinstance(self.security_method, BasicAuth):
                    dependencies = [Depends(self.security_method.basic_auth_required)]
            else:
                dependencies = []

            # Register the route with the router
            self.router.add_api_route(path, func, methods=methods, dependencies=dependencies)

        return decorator
