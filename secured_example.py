from apispark.app import ApiSparkApp
from apispark.auth import Auth
from pydantic import BaseModel

# Create an instance of the ApiSparkApp class with JWT authentication enabled
app = ApiSparkApp(globals(), security="jwt", secret="my_secret_key")

# Create an instance of the Auth class with OAuth2 authentication enabled
# using Google as the provider and custom client ID and client secret
auth = Auth(oauth2=True, provider="google", client_id="my_client_id", client_secret="my_client_secret")

# Create an instance of the ApiSparkApp class with API key authentication enabled
# using a custom list of valid API keys
app = ApiSparkApp(globals(), security="apikey", valid_keys=["key1", "key2", "key3"])

# Create an instance of the ApiSparkApp class with basic authentication enabled
# using a custom dictionary of valid username-password pairs
app = ApiSparkApp(globals(), security="basic", valid_users={"user1": "password1", "user2": "password2"})

# Define a Pydantic model for the item data
class Item(BaseModel):
    name: str
    price: float

# Define a route for getting an item by ID
def get_item(item_id: int):
    return {"item_id": item_id, "name": "Example"}

# Define a route for adding a new item with authentication required
# using the security method specified when creating the ApiSparkApp instance
def post_item(item: Item, auth=auth):
    return {"message": f"Item {item.name} added"}

# Run the FastAPI application
app.run()
