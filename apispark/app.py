from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from apispark.auth import Auth
from apispark.routers.router import Router
from apispark.middleware import MiddlewareManager
from apispark.exceptions.exception_handler import custom_exception_handler, http_exception_handler

class ApiSparkApp:
    def __init__(self, security=None, **kwargs):
        """
        Initialize an ApiSparkApp instance.

        Args:
            security (str): The type of security to use. Options are "apikey", "basic", "jwt", or "oauth2".
            **kwargs: Keyword arguments to pass to the Auth class initializer.

        Returns:
            None
        """
        self.app = FastAPI()
        self.router = Router()
        self.middleware_manager = MiddlewareManager()
        self.auth = Auth(security, **kwargs)
        self.middleware_manager.register_middlewares(self.app)
        self._add_health_check()
        self._register_exception_handlers()
        self.router.include_in_app(self.app)

    def get_app(self):
        """
        Return the FastAPI app instance.

        Returns:
            fastapi.FastAPI: The FastAPI app instance.
        """
        return self.app

    def _add_health_check(self):
        @self.app.get("/health", tags=["Health"])
        async def health_check():
            """
            A health check endpoint.

            Returns a JSON response with a status of "healthy" and a message indicating that the API is running properly.

            Tags:
                Health
            """
            return JSONResponse(content={"status": "healthy", "message": "API is running properly."})

    def _register_exception_handlers(self):
        """
        Register custom exception handlers for the FastAPI app.

        This method registers exception handlers for the following exceptions:
        - Exception: Handled by custom_exception_handler
        - HTTPException: Handled by http_exception_handler
        """
        self.app.add_exception_handler(Exception, custom_exception_handler)
        self.app.add_exception_handler(HTTPException, http_exception_handler)

    def add_cors(self, allow_origins=["*"], allow_methods=["GET", "POST"]):
        """
        Enable CORS support for the FastAPI app.

        By default, this method sets the following configuration for CORS:
        - Allow origins: *
        - Allow methods: GET, POST
        - Allow credentials: True
        - Allow headers: *

        You can customize the configuration by passing in the desired values for
        `allow_origins`, `allow_methods`, `allow_credentials`, and `allow_headers`.

        Args:
            allow_origins (list[str], optional): A list of allowed origins. Defaults to ["*"].
            allow_methods (list[str], optional): A list of allowed methods. Defaults to ["GET", "POST"].

        Returns:
            None
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=allow_methods,
            allow_headers=["*"],
        )

    def serve_static(self, path, directory):
        """
        Serve static files from the specified directory.

        This method mounts a StaticFiles endpoint to the specified path and
        serves the static files from the specified directory.

        Args:
            path (str): The path at which to serve the static files.
            directory (str): The directory containing the static files.

        Returns:
            None
        """
        self.app.mount(path, StaticFiles(directory=directory), name="static")