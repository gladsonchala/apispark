import inspect
from fastapi import APIRouter

class Router:
    def __init__(self):
        self.router = APIRouter()

    def register_routes(self, module_globals):
        for name, func in module_globals.items():
            if inspect.isfunction(func):
                if name.startswith('get_'):
                    self.router.get(f"/{name[4:]}")(func)
                elif name.startswith('post_'):
                    self.router.post(f"/{name[5:]}")(func)
                elif name.startswith('put_'):
                    self.router.put(f"/{name[4:]}")(func)
                elif name.startswith('delete_'):
                    self.router.delete(f"/{name[7:]}")(func)

    def include_in_app(self, app):
        app.include_router(self.router)
