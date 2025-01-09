from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.domain.models.models import Order, Product, User, OrderItem
from app.domain.controllers.users_endP import get_current_user
from typing import List
from app.utils.database.session import get_db
from sqlalchemy import func


router = APIRouter()

@router.get("/reports/sales/total")
def get_total_sales(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")
    total_sales = db.query(Order).filter(Order.status == "completed").count()
    return {"message": f"Las ventas totales son: {total_sales}"}

@router.get("/reports/sales/{product_id}")
def get_sales_by_product(product_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")
    total_sales = (db.query(OrderItem).join(Order, OrderItem.order_id == Order.id).filter(OrderItem.product_id == product_id, Order.status == "completed").count())
    if not total_sales:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not sales found")
    return {"total_sales": total_sales}

@router.get("/reports/profit/total")
def get_total_profit(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    total_profit = (
        db.query(func.sum(OrderItem.quantity * (Order.total_amount - Product.cost)))
        .join(Product, OrderItem.product_id == Product.id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.status == "completed")
        .first()
    )
    return {"total_profit": total_profit[0]}

@router.get("/reports/profit/{product_id}")
def get_total_profit(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    total_profit = (
        db.query(Product.name, func.sum(OrderItem.quantity * (Product.price - Product.cost)))
        .join(Product, OrderItem.product_id == Product.id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.status == "completed")
        .group_by(Product.id)
    )
    if total_profit:
        total_profit_list = []
        for product, totalProfit in total_profit:
            total_profit_list.append({
                "name": product,
                "total_profit": totalProfit
            })
        return {"total_profit": total_profit_list}
    else:
        return {"message": "Product not found"}


@router.get("/customers/top")
def get_top_customers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")

    top_customers = (
        db.query(User, func.sum(Order.total_amount).label("total_spent"))
        .join(Order, User.id == Order.user_id)
        .filter(User.role == "customer", Order.status == "completed")
        .group_by(User.id)
        .order_by(func.sum(Order.total_amount).desc())
        .limit(5)
        .all()
    )
    if top_customers:
        top_customers_list = []
        for customer, total_spent in top_customers:
            top_customers_list.append({
                "username": customer.username,
                "total_spent": total_spent
            })
        return {"top_customers": top_customers_list}
    else:
        return {"message": "Customers not found"}
    
@router.get("/products/top")
def get_top_product(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")

    top_product = (
        db.query(Product.name, func.sum(OrderItem.quantity).label("total_quantity"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order,  OrderItem.order_id ==  Order.id)
        .filter(Order.status == "completed")
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    if top_product:
        top_product_list = []
        for product, total_quantity in top_product:
            top_product_list.append({
                "name": product,
                "total_spent": total_quantity
            })
        return {"top_product": top_product_list}
    else:
        return {"message": "Product not found"}

