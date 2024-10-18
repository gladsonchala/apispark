from fastapi import FastAPI
from apispark.routers.router import Router

app = FastAPI()

# Initialize apispark Router
router = Router()

# Developer's route functions
async def get_users():
    return {"message": "Listing all users"}

async def post_user():
    return {"message": "Creating a new user"}

async def get_user_by_id(user_id: int):
    return {"message": f"Getting user with ID {user_id}"}

async def put_user(user_id: int):
    return {"message": f"Updating user with ID {user_id}"}

async def delete_user(user_id: int):
    return {"message": f"Deleting user with ID {user_id}"}

# Register routes from this module
router.register_routes(globals())

# Include the router in the FastAPI app
router.include_in_app(app)

# Run the app with `uvicorn example_project.app:app --reload`
