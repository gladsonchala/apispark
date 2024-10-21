from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from apispark.auth import Auth
from apispark.routers.router import Router
from apispark.middleware import MiddlewareManager
from apispark.exceptions.exception_handler import custom_exception_handler, http_exception_handler

class ApiSparkApp:
    def __init__(self, security=None, **kwargs):
        self.app = FastAPI()
        self.router = Router()
        self.middleware_manager = MiddlewareManager()

        # Initialize Auth based on security type
        self.auth = Auth(security, **kwargs)

        # Middleware and exception handling setup
        self.middleware_manager.register_middlewares(self.app)
        self._add_health_check()
        self._register_exception_handlers()

    def get_app(self):
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
