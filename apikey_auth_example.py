from apispark.app import ApiSparkApp
from pydantic import BaseModel

# Create an instance of the ApiSparkApp with API Key authentication
app_instance = ApiSparkApp(globals(), security="apikey", valid_keys=["my_secret_key"])

# Get the FastAPI application instance
app = app_instance.get_app()

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float

# Automatically registered route for getting items (open route)
def get_items():
    return {"message": "Fetching all items"}

# Automatically registered POST route for adding an item (protected by API key)
def post_item(item: Item):
    return {"message": f"Item {item.name} added"}
post_item.protected = True  # Mark the route as protected by the API key
