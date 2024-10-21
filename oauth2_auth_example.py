from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import Depends

app_instance = ApiSparkApp(
    security="oauth2",
    provider="google",
    client_id="your_google_client_id",
    client_secret="your_google_client_secret"
)
app = app_instance.get_app()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

@app.post("/item")
def post_item(item: Item, token: str = Depends(app_instance.auth.login_required)):
    return {"message": f"Item {item.name} added"}
