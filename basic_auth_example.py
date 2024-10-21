from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import Depends

# Create an instance of the ApiSparkApp with Basic authentication
app_instance = ApiSparkApp(security="basic", valid_users={"admin": "password"})

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

# Automatically registered POST route for adding an item (protected by Basic Auth)
@app.post("/item")
def post_item(item: Item, auth: str = Depends(app_instance.auth.basic_auth_required)):
    return {"message": f"Item {item.name} added"}
