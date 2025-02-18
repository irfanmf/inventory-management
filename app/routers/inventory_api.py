from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryResponse, InventoryMove, ItemInventoryRequest, UpdateStockRequest, WarehouseInventoryRequest, WarehouseItemRequest
import uuid

router = APIRouter(prefix="/inventory", tags=["Inventory"])

# Get all inventory in a warehouse
@router.post("/warehouse", response_model=list[InventoryResponse])
def get_inventory_by_warehouse(request: WarehouseInventoryRequest, db: Session = Depends(get_db)):
    inventory_items = db.query(Inventory).filter(Inventory.warehouse_id == request.warehouse_id).all()
    return inventory_items

# Get item information across warehouses
@router.post("/item", response_model=list[InventoryResponse])
def get_item_across_warehouses(request: ItemInventoryRequest, db: Session = Depends(get_db)):
    inventory_items = db.query(Inventory).filter(Inventory.item_id == request.item_id).all()
    return inventory_items

# Get item information in a specific warehouse
@router.post("/warehouse/item", response_model=InventoryResponse)
def get_item_in_warehouse(request: WarehouseItemRequest, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(
        Inventory.warehouse_id == request.warehouse_id,
        Inventory.item_id == request.item_id
    ).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found in warehouse")
    return inventory_item

# Update stock quantity
@router.post("/update-stock")
def update_stock(request: UpdateStockRequest, db: Session = Depends(get_db)):
    # Check if the inventory exists
    inventory_item = db.query(Inventory).filter(
        Inventory.warehouse_id == request.warehouse_id,
        Inventory.item_id == request.item_id
    ).first()

    if inventory_item:
        # Update existing stock
        inventory_item.quantity = request.quantity
    else:
        # Create new inventory entry if not found
        inventory_item = Inventory(
            warehouse_id=request.warehouse_id,
            item_id=request.item_id,
            quantity=request.quantity
        )
        db.add(inventory_item)

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