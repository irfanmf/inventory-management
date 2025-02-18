import uuid
from sqlalchemy import UUID, Column, String
from app.database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    location = Column(String, nullable=True)