from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class InventoryBase(BaseModel):
    product_id: UUID
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiar de orm_mode a from_attributes

class InventoryInDB(Inventory):
    pass