from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class OrderItemBase(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiar de orm_mode a from_attributes