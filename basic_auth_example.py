from apispark.app import ApiSparkApp
from pydantic import BaseModel

# Create an instance of the ApiSparkApp class with Basic authentication enabled
app_instance = ApiSparkApp(globals(), security="basic", valid_users={"admin": "password"})

# Get the FastAPI application instance
app = app_instance.get_app()

# Define a Pydantic model for the item data
class Item(BaseModel):
    name: str
    price: float

# Define a protected route for adding a new item
@app_instance.route("/items", methods=["POST"], protected=True)
async def post_item(item: Item):
    return {"message": f"Item {item.name} added"}
