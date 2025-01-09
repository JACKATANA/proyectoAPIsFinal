from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    code: str
    name: str
    description: str
    cost: float
    margin: float
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Cambiar de orm_mode a from_attributes

class ProductInDB(Product):
    pass