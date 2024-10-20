from fastapi import FastAPI, Depends
from apispark.routers.router import Router
from apispark.auth import Auth

app = FastAPI()

# Create an Auth instance with API Key authentication
auth = Auth(security="apikey", valid_keys=["my_secret_key"])

# Create an instance of your Router class
router = Router()

# Register your routes with the auth instance
router.register_routes(globals(), auth=auth)

# Include the router in the FastAPI app
router.include_in_app(app)

@app.get("/unprotected")
async def unprotected_route():
    return {"message": "This is an unprotected route"}

@app.get("/protected")
async def protected_route(api_key=Depends(auth.api_key_required)):
    return {"message": "This is a protected route"}
