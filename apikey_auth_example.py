from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import APIRouter, Depends

# Create an instance of the ApiSparkApp with API Key authentication
app_instance = ApiSparkApp(security="apikey", valid_keys=["my_secret_key"])

# Get the FastAPI application instance
app = app_instance.get_app()

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float

# Automatically registered route for getting items (open route)
@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

# Automatically registered POST route for adding an item (protected by API key)
@app.post("/item")
def post_item(item: Item, api_key: str = Depends(app_instance.auth.api_key_required)):
    return {"message": f"Item {item.name} added"}
