from apispark.app import ApiSparkApp
from pydantic import BaseModel

# Create an instance of the ApiSparkApp with Basic authentication
app_instance = ApiSparkApp(globals(), security="basic", valid_users={"admin": "password"})

# Get the FastAPI application instance
app = app_instance.get_app()

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float

# Automatically registered route for fetching all items (open route)
def get_items():
    return {"message": "Fetching all items"}

# Automatically registered POST route for adding an item (protected by Basic Auth)
def post_item(item: Item):
    return {"message": f"Item {item.name} added"}
post_item.protected = True  # Mark the route as protected by Basic Auth
