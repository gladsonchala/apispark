from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import Depends

# Create an instance of the ApiSparkApp with JWT authentication
app_instance = ApiSparkApp(
    security="jwt",
    secret="your_secret_key",
    authorizationUrl="your_authorization_url",  # Replace with your actual authorization URL
    tokenUrl="your_token_url"                   # Replace with your actual token URL
)

# Get the FastAPI application instance
app = app_instance.get_app()

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float

# Automatically registered route for fetching all items (open route)
@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

# Automatically registered POST route for adding an item (protected by JWT)
@app.post("/item")
def post_item(item: Item, token: str = Depends(app_instance.auth.jwt_required)):
    return {"message": f"Item {item.name} added"}
