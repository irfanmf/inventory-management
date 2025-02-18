from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryResponse, InventoryCreate, InventoryMove
import uuid

router = APIRouter(prefix="/inventory", tags=["Inventory"])

# Get all inventory in a warehouse
@router.get("/{warehouse_id}", response_model=list[InventoryResponse])
def get_inventory_by_warehouse(warehouse_id: uuid.UUID, db: Session = Depends(get_db)):
    inventory_items = db.query(Inventory).filter(Inventory.warehouse_id == warehouse_id).all()
    return inventory_items

# Get item information across warehouses
@router.get("/item/{item_id}", response_model=list[InventoryResponse])
def get_item_across_warehouses(item_id: uuid.UUID, db: Session = Depends(get_db)):
    inventory_items = db.query(Inventory).filter(Inventory.item_id == item_id).all()
    return inventory_items

# Get item information in a specific warehouse
@router.get("/{warehouse_id}/item/{item_id}", response_model=InventoryResponse)
def get_item_in_warehouse(warehouse_id: uuid.UUID, item_id: uuid.UUID, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id, Inventory.item_id == item_id
    ).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found in warehouse")
    return inventory_item

# Update stock quantity
@router.put("/{warehouse_id}/item/{item_id}")
def update_stock(warehouse_id: uuid.UUID, item_id: uuid.UUID, quantity: int, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(
        Inventory.warehouse_id == warehouse_id, Inventory.item_id == item_id
    ).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found in warehouse")
    
    inventory_item.quantity += quantity  # Adjust stock
    db.commit()
    db.refresh(inventory_item)
    return {"message": "Stock updated", "data": inventory_item}

# Move stock from one warehouse to another
@router.post("/move", response_model=InventoryResponse)
def move_inventory(move_data: InventoryMove, db: Session = Depends(get_db)):
    source_item = db.query(Inventory).filter(
        Inventory.warehouse_id == move_data.source_warehouse_id,
        Inventory.item_id == move_data.item_id
    ).first()
    
    if not source_item or source_item.quantity < move_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock to move")
    
    # Reduce stock from source
    source_item.quantity -= move_data.quantity

    # Find or create inventory record in destination warehouse
    dest_item = db.query(Inventory).filter(
        Inventory.warehouse_id == move_data.destination_warehouse_id,
        Inventory.item_id == move_data.item_id
    ).first()
    
    if dest_item:
        dest_item.quantity += move_data.quantity
    else:
        dest_item = Inventory(
            id=uuid.uuid4(),
            warehouse_id=move_data.destination_warehouse_id,
            item_id=move_data.item_id,
            quantity=move_data.quantity
        )
        db.add(dest_item)

    db.commit()
    db.refresh(dest_item)
    
    return dest_item