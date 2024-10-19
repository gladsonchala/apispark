from apispark.app import ApiSparkApp
from pydantic import BaseModel

app_instance = ApiSparkApp(globals(), security="apikey", valid_keys=["my_secret_key"])
app = app_instance.get_app()

class Item(BaseModel):
    name: str
    price: float

@app_instance.route("/items", methods=["POST"], protected=True)
async def post_item(item: Item):
    return {"message": f"Item {item.name} added"}
