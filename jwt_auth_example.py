from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import Depends

app_instance = ApiSparkApp(
    security="jwt",
    secret="your_secret_key",
    authorizationUrl="your_authorization_url",
    tokenUrl="your_token_url"
)
app = app_instance.get_app()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

@app.post("/item")
def post_item(item: Item, token: str = Depends(app_instance.auth.jwt_required)):
    return {"message": f"Item {item.name} added"}
