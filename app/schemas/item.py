from uuid import UUID
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: UUID
    class Config:
        from_attributes = True
