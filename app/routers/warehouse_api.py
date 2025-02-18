from fastapi import APIRouter, Depends
from app.models.warehouse import Warehouse
from app.database import SessionLocal, get_db
from app.schemas.warehouse import WarehouseResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/warehouse", tags=["warehouse"])

@router.get("/warehouses", response_model=list[WarehouseResponse])
def get_all_warehouses(db: Session = Depends(get_db)):
    warehouses = db.query(Warehouse).all()
    return warehouses