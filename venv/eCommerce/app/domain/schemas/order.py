from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    canceled = "canceled"

class OrderBase(BaseModel):
    user_id: UUID
    total_amount: float
    status: OrderStatus

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: OrderStatus

class Order(OrderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiar de orm_mode a from_attributes

class OrderInDB(Order):
    pass