from fastapi import APIRouter

class Router:
    def __init__(self):
        self.router = APIRouter()

    def include_in_app(self, app):
        app.include_router(self.router)
