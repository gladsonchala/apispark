from fastapi import FastAPI
from .logging_middleware import LoggingMiddleware

class MiddlewareManager:
    def __init__(self):
        self.middlewares = [
            LoggingMiddleware,
        ]

    def register_middlewares(self, app: FastAPI):
        for middleware in self.middlewares:
            app.add_middleware(middleware)

    def add_middleware(self, middleware_class):
        self.middlewares.append(middleware_class)
