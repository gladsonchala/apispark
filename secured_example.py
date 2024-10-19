from apispark.app import ApiSparkApp
from apispark.auth.jwt_auth import JWTAuth
from pydantic import BaseModel

# Create an instance of the ApiSparkApp class with JWT authentication enabled
app_instance = ApiSparkApp(globals(), security="jwt", secret="my_secret_key")

# Get the FastAPI application instance
app = app_instance.get_app()

# Create an instance of the JWTAuth class
jwt_auth = JWTAuth(secret="my_secret_key")

# Define a Pydantic model for the item data
class Item(BaseModel):
    name: str
    price: float

# Define a route for getting an item by ID
def get_item(item_id: int):
    return {"item_id": item_id, "name": "Example"}

# Define a route for adding a new item with authentication required
# using the security method specified when creating the ApiSparkApp instance
def post_item(item: Item):
    return {"message": f"Item {item.name} added"}


