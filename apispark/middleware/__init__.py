from fastapi import FastAPI
from .logging_middleware import LoggingMiddleware

class MiddlewareManager:
    """
    This class manages the automatic registration of middleware in the FastAPI app.
    """
    def __init__(self):
        self.middlewares = [
            LoggingMiddleware,  # Add logging middleware by default
        ]

    def register_middlewares(self, app: FastAPI):
        """
        Register all middlewares in the app.
        """
        for middleware in self.middlewares:
            app.add_middleware(middleware)

    def add_middleware(self, middleware_class):
        """
        Allow developers to add custom middleware.
        """
        self.middlewares.append(middleware_class)
