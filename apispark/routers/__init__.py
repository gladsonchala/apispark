import inspect
import importlib
import os
from fastapi import APIRouter
from apispark.auth import Auth

router = APIRouter()

def register_routes():
    routers_directory = os.path.dirname(__file__)
    for filename in os.listdir(routers_directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"apispark.routers.{module_name}")
            for name, function in inspect.getmembers(module, inspect.isfunction):
                if name.startswith("get_"):
                    route_path = f"/{module_name}/{name[4:]}"
                    router.get(route_path)(auth.api_key_required(function) if auth else function)
                elif name.startswith("post_"):
                    route_path = f"/{module_name}/{name[5:]}"
                    router.post(route_path)(auth.api_key_required(function) if auth else function)
                elif name.startswith("put_"):
                    route_path = f"/{module_name}/{name[4:]}"
                    router.put(route_path)(auth.api_key_required(function) if auth else function)
                elif name.startswith("delete_"):
                    route_path = f"/{module_name}/{name[7:]}"
                    router.delete(route_path)(auth.api_key_required(function) if auth else function)
