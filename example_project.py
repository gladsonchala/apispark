from apispark.app import ApiSparkApp
from apispark.auth import Auth
from pydantic import BaseModel

app = ApiSparkApp(globals())
auth = Auth(oauth2=True)

class Item(BaseModel):
    name: str
    price: float

def get_item(item_id: int):
    return {"item_id": item_id, "name": "Example"}

def post_item(item: Item, auth=auth):
    return {"message": f"Item {item.name} added"}

app.run()
