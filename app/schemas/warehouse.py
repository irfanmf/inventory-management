from uuid import UUID
from pydantic import BaseModel


class WarehouseBase(BaseModel):
    name: str
    location: str

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    id: UUID
    class Config:
        from_attributes = True