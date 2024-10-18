from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .routers.router import Router
from .middleware import MiddlewareManager
from .exceptions.exception_handler import custom_exception_handler, http_exception_handler

class ApiSparkApp:
    """
    This class provides a convenient wrapper for creating FastAPI applications 
    and auto-registering routes based on naming conventions.
    """
    def __init__(self, module_globals):
        self.app = FastAPI()
        self.router = Router()
        self.middleware_manager = MiddlewareManager()  # Middleware manager instance

        self.router.register_routes(module_globals)
        self.middleware_manager.register_middlewares(self.app)  # Register middleware
        self._add_health_check()

        # Register custom exception handlers
        self._register_exception_handlers()

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
