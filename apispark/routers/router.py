# apispark/routers/router.py

from fastapi import APIRouter, Depends,Query, Path, Body

import inspect

class Router:
    def __init__(self):
        self.router = APIRouter()


    def register_routes(self, module_globals):
        for name, func in module_globals.items():
            if inspect.isfunction(func):
                sig = inspect.signature(func)
                params = []
                for param_name, param in sig.parameters.items():
                    if param.default is param.empty:
                        params.append(Path(...))
                    else:
                        params.append(Query(...))

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
