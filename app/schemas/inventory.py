from uuid import UUID
from pydantic import BaseModel


class InventoryBase(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryMove(BaseModel):
    source_warehouse_id: UUID
    destination_warehouse_id: UUID
    item_id: UUID
    quantity: int

class InventoryResponse(InventoryBase):
    id: UUID
    class Config:
        from_attributes = True