from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.domain.models.models import User, Inventory, Product
from app.utils.database.session import get_db
from app.domain.services.security import secret_key
from datetime import timedelta
from app.domain.controllers.users_endP import oauth2_scheme
from app.domain.schemas.inventory import InventoryCreate, InventoryUpdate

router = APIRouter()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
        

@router.get("/inventories/{product_id}")
async def get_inventory(product_id: str,current_user: User = Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user.role=="manager":
        inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
        product_name= db.query(Product).filter(Product.id == product_id).first()
        return {"message": f"La cantidad en inventario del producto {product_name.name} es {inventory.quantity}"}
    else:
        raise HTTPException(status_code=401, detail="Inventory can only be accessed by Managers", headers={"WWW-Authenticate": "Bearer"})

@router.post("/inventories/{product_id}")
async def add_inventory(product_id: str, inventory_in: InventoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is already an inventory with this product")

    if (inventory_in.quantity <= 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The quantity must be greater than 0")
    inventory = Inventory(product_id=product.id, quantity=inventory_in.quantity)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

@router.put("/inventories/{product_id}")
def update_inventory(product_id: str, inventory_in: InventoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    for key, value in inventory_in.dict().items():
        if key == "product_id":
            id_product = product_id
            setattr(inventory, "product_id", id_product)
        else:
            setattr(inventory, key, value)
    db.commit()
    db.refresh(inventory)
    return inventory