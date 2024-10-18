from apispark.app import ApiSparkApp

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

# Create an ApiSparkApp instance and pass the module globals for route detection
app_instance = ApiSparkApp(globals())

# Get the FastAPI app instance
app = app_instance.get_app()

# Run with `uvicorn example_project.app:app --reload`
