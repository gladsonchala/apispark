from apispark.app import ApiSparkApp
from pydantic import BaseModel

# Create an instance of the ApiSparkApp with OAuth2 authentication
app_instance = ApiSparkApp(
    globals(),
    security="oauth2",
    provider="google",
    client_id="your_google_client_id",
    client_secret="your_google_client_secret"
)

# Get the FastAPI application instance
app = app_instance.get_app()

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float

# Automatically registered route for getting items (open route)
def get_items():
    return {"message": "Fetching all items"}

# Automatically registered POST route for adding an item (protected by OAuth2)
def post_item(item: Item):
    return {"message": f"Item {item.name} added"}
post_item.protected = True  # Mark the route as protected by OAuth2
