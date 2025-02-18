from fastapi import APIRouter, Depends
from app.models.item import Item
from app.database import SessionLocal, get_db
from app.schemas.item import ItemResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/item", tags=["item"])

@router.post("/items", response_model=list[ItemResponse])
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items