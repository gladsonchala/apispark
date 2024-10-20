import inspect
from fastapi import APIRouter, Depends

class Router:
    def __init__(self):
        self.router = APIRouter()

    def register_routes(self, module_globals, auth=None):
        for name, func in module_globals.items():
            if inspect.isfunction(func):
                # Automatically determine route path and HTTP method
                if name.startswith('get_'):
                    self._register_route('get', f"/{name[4:]}", func, auth)
                elif name.startswith('post_'):
                    self._register_route('post', f"/{name[5:]}", func, auth)
                elif name.startswith('put_'):
                    self._register_route('put', f"/{name[4:]}", func, auth)
                elif name.startswith('delete_'):
                    self._register_route('delete', f"/{name[7:]}", func, auth)

    def _register_route(self, method, path, func, auth):
        # Apply security if the route is protected
        dependencies = []
        if getattr(func, "protected", False) and auth:
            if auth.security == "jwt":
                dependencies.append(Depends(auth.jwt_required))
            elif auth.security == "oauth2":
                dependencies.append(Depends(auth.login_required))
            elif auth.security == "apikey":
                dependencies.append(Depends(auth.api_key_required))
            elif auth.security == "basic":
                dependencies.append(Depends(auth.basic_auth_required))

        # Register the route
        getattr(self.router, method)(path, dependencies=dependencies)(func)

    def include_in_app(self, app):
        app.include_router(self.router)
