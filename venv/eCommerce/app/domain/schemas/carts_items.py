from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CartItemBase(BaseModel):
    cart_id: UUID
    product_id: UUID
    quantity: int

class CartItemCreate(BaseModel):
     quantity: int


class CartItemUpdate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiar de orm_mode a from_attributes

class CartITemInDB(CartItem):
    pass