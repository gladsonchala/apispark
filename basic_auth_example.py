from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import Depends

app_instance = ApiSparkApp(security="basic", valid_users={"admin": "password"})
app = app_instance.get_app()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

@app.post("/item")
def post_item(item: Item, auth: str = Depends(app_instance.auth.basic_auth_required)):
    return {"message": f"Item {item.name} added"}
