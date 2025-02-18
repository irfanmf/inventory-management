from fastapi import FastAPI
from app.database import engine, Base
from app.routers import inventory_api, item_api, warehouse_api
from app.models import inventory, item, warehouse


app = FastAPI(title="Inventory Management API", version="1.0")

Base.metadata.create_all(bind=engine)

app.include_router(inventory_api.router)
app.include_router(warehouse_api.router)
app.include_router(item_api.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Inventory Management API"}
