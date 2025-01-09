from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import join
from app.domain.models.models import User, Product, Cart, CartItem, Inventory
from app.utils.database.session import get_db
from app.utils.database.database import Base
from app.domain.schemas.carts import CartCreate
from app.domain.schemas.carts_items import CartItemCreate, CartItemUpdate
from app.domain.controllers.users_endP import get_current_user

router = APIRouter()
oauth2_scheme= OAuth2PasswordBearer("/users/login")

@router.post("/carts/register")
def create_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    if(db.query(Cart).filter(Cart.user_id == current_user.id).first()):
        raise HTTPException(status_code=409, detail="The cart has already been created.")
    cart = Cart(user_id=current_user.id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


@router.post("/carts/items/register/{product_id}")
def add_item_to_cart(product_id:str, cart_item: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found",
        )
    if (cart_item.quantity <= 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The quantity must be greater than 0",
        )
    inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()      
    if not inventory or inventory.quantity==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product out of stock",
        )
    if ( inventory.quantity<cart_item.quantity):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is not enough stock for this product",
        )
    item=db.query(CartItem).filter(CartItem.product_id == product.id, CartItem.cart_id==cart.id).first()    
    if item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The product already exists in your cart.",
        )  
    cart_item = CartItem(cart_id=cart.id,
                               product_id=product.id,
                               quantity=cart_item.quantity)
    
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/carts")
async def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart:
        cart_items = (db.query(CartItem.id, Product.name, CartItem.quantity).join(Product, CartItem.product_id == Product.id).filter(CartItem.cart_id == cart.id).all())
        product_info = [f"{item.name} (x{item.quantity})" for item in cart_items] 
        return {"message": f"The products in the carts are: {', '.join(product_info)}"}
    else:
        raise HTTPException(status_code=401, detail="Cart not found", headers={"WWW-Authenticate": "Bearer"})

@router.put("/items/{product_id}")
def update_cart_item(product_id: str, cart_in: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cart not found")
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    product = db.query(Product).filter(Product.id == product_id).first()
    if (cart_in.quantity <= 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The quantity must be greater than 0",
        )
    inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()      
    if not inventory or inventory.quantity==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product out of stock",
        )
    if ( inventory.quantity<cart_item.quantity):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is not enough stock for this product",
        )
    for key, value in cart_in.dict().items():
            setattr(cart_item, key, value)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/items/{product_id}")
def delete_cart_item(product_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cart not found")
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return cart_item
