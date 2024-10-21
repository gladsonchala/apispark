from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import APIRouter, Depends

app_instance = ApiSparkApp(security="apikey", valid_keys=["my_secret_key"])
app = app_instance.get_app()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

@app.post("/item")
def post_item(item: Item, api_key: str = Depends(app_instance.auth.api_key_required)):
    return {"message": f"Item {item.name} added"}
