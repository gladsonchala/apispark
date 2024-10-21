from apispark.app import ApiSparkApp
from pydantic import BaseModel
from fastapi import Depends
from datetime import timedelta

# Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app_instance = ApiSparkApp(
    security="jwt",
    secret=SECRET_KEY,
    algorithm=ALGORITHM,
    authorizationUrl="your_authorization_url",
    tokenUrl="your_token_url"
)
app = app_instance.get_app()

class Item(BaseModel):
    name: str
    price: float

class Token(BaseModel):
    access_token: str
    token_type: str

@app.get("/items")
def get_items():
    return {"message": "Fetching all items"}

@app.post("/item")
def post_item(item: Item, token: str = Depends(app_instance.auth.jwt_required)):
    return {"message": f"Item {item.name} added"}

@app.post("/token", response_model=Token)
async def login_for_access_token():
    # Assuming authentication is successful
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = app_instance.auth.jwt_auth.create_access_token(
        data={"sub": "user_id"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
