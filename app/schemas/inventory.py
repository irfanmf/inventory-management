from uuid import UUID
from pydantic import BaseModel


class InventoryBase(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    quantity: int

class WarehouseInventoryRequest(BaseModel):
    warehouse_id: UUID

class ItemInventoryRequest(BaseModel):
    item_id: UUID

class WarehouseItemRequest(BaseModel):
    warehouse_id: UUID
    item_id: UUID

class UpdateStockRequest(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    quantity: int

class InventoryMove(BaseModel):
    source_warehouse_id: UUID
    destination_warehouse_id: UUID
    item_id: UUID
    quantity: int

class WarehouseInventoryResponse(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    item_name: str  # Include item name
    quantity: int

class ItemInventoryResponse(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    item_name: str  # Required field
    quantity: int

class InventoryResponse(InventoryBase):
    id: UUID
    class Config:
        from_attributes = True