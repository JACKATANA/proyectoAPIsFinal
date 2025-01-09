from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import join
from app.domain.models.models import User, Product, Cart, CartItem, Inventory, Order, OrderItem
from app.utils.database.session  import get_db
from app.domain.controllers.users_endP import get_current_user
from app.domain.schemas.order import OrderUpdate
from sqlalchemy import exc


router = APIRouter()

@router.post("/orders")
def create_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role!= "customer":
        raise HTTPException(status_code=400, detail="Only customers can create orders") 
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart:
        order_old = db.query(Order).filter(Order.user_id == current_user.id, Order.status=="pending").first()
        if order_old:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You have a pending order",
            )
        cart_items = (db.query(CartItem.id, Product.name, CartItem.quantity, Product.price).join(Product, CartItem.product_id == Product.id).filter(CartItem.cart_id == cart.id).all())
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no products in the cart",
            )
        total_amount = sum(item.price * item.quantity for item in cart_items) 
        order = Order(user_id=current_user.id, total_amount=total_amount, status="pending")
        db.add(order)
        db.commit()
        db.refresh(order)
        order_new= (db.query(Order).filter(Order.user_id == cart.user_id,Order.status=="pending").first())
        order_items= (db.query(CartItem).filter(CartItem.cart_id == cart.id).all())
        for item in order_items:
            if item.cart_id == cart.id:
                orderItem= OrderItem(order_id=order_new.id, product_id=item.product_id, quantity=item.quantity)
                db.add(orderItem)
                db.commit()
                db.refresh(orderItem)
        return order
    else:
        raise HTTPException(status_code=401, detail="Cart not found", headers={"WWW-Authenticate": "Bearer"})
    
@router.get("/orders/{user_id}")
def read_orders(user_id: str,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):  
    if current_user.role!= "manager":
        raise HTTPException(status_code=400, detail="Only managers can access")
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

@router.get("/order/{order_id}")
def read_order(order_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role!= "manager":
        raise HTTPException(status_code=400, detail="Only managers can access")
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order

@router.put("/orders/{order_id}")
def update_order(order_id: str, order_in: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    if order.status!="pending":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only pending orders can be modified",
        )
    for key, value in order_in.dict().items():
            setattr(order, key, value)
    db.commit()
    if order_in.status=="completed":
     cart = db.query(Cart).filter(Cart.user_id == order.user_id).first() 
     cart_items = db.query(CartItem.product_id, CartItem.quantity).filter(CartItem.cart_id == cart.id).all()
     for product_id, quantity in cart_items:
                inventory_item = db.query(Inventory).filter(Inventory.product_id == product_id).first()
                if inventory_item:
                    inventory_item.quantity -= quantity
                    if inventory_item.quantity < 0:
                        db.rollback()
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No enough stock for product {product_id}")     
     cart_items_to_delete = (
            db.query(CartItem)
            .filter(CartItem.cart_id == cart.id)
            .delete()
        )
     db.commit()
     return order