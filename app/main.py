from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router
from app.models import inventory, item, warehouse


app = FastAPI(title="Inventory Management API", version="1.0")

Base.metadata.create_all(bind=engine)

app.include_router(router.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Inventory Management API"}
