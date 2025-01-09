from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CartBase(BaseModel):
    user_id: UUID

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass

class Cart(CartBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiar de orm_mode a from_attributes

class CartInDB(Cart):
    pass