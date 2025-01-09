from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils.database.database import engine
from sqlalchemy.orm import Session
from app.domain.models.models import User, Product
from app.utils.database.session import get_db
from app.domain.schemas.product import ProductCreate, ProductUpdate
from app.domain.controllers.users_endP import get_current_user
from app.domain.services.calculate_price import final_price

router = APIRouter()
oauth2_scheme= OAuth2PasswordBearer("/users/login")

@router.post("/products/register")
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    if(db.query(Product).filter(Product.code == product.code).first()):
        raise HTTPException(status_code=409, detail="There is already a product with this code.")
    if(db.query(Product).filter(Product.name == product.name).first()):
        raise HTTPException(status_code=409, detail="There is already a product with this name.")
    db_product = Product(
        code=product.code,
        name=product.name,
        description=product.description,
        cost=product.cost,
        margin=product.margin,
        price=final_price(product.cost,product.margin),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/product")
async def get_product(db:Session=Depends(get_db)):
    data=db.query(Product).all()
    product_code = []  
    for product in data:
        product_code.append(product.code)  
        
    print(product_code) 
    return data

@router.get("/product/{product_code}")
async def get_product(product_code: str, db: Session = Depends(get_db)):
    data = db.query(Product).filter(Product.code == product_code).first()  
    if data is None:
        raise HTTPException(status_code=400, detail= "The product does not exist.")
    return data

@router.put("/product/{product_code}")
async def update_product(product_code: str, product_update: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.code == product_code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    for key, value in product_update.dict().items():
        setattr(product, key, value)
    product.price=final_price(product.cost,product.margin)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/delete/{product_code}")
def delete_product(product_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    product = db.query(Product).filter(Product.code == product_code).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    db.delete(product)
    db.commit()
    return product