from fastapi import APIRouter
import inspect

class Router:
    def __init__(self):
        self.router = APIRouter()

    def register_routes(self, module_globals):
        """
        Automatically register functions with 'get_', 'post_', 'put_', or 'delete_' 
        prefixes as FastAPI routes based on their HTTP method.
        """
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
        """
        Include the registered router in the FastAPI app.
        """
        app.include_router(self.router)
