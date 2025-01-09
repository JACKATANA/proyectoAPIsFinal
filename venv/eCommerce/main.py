from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.domain.controllers import users_endP,inventory_endP,product_endP, carts_endP, orders_endP, reports_endP
from app.utils.database.database import Base, engine 

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return "Bienvenido al sistema de venta de productos electronicos"

app.include_router(users_endP.router, tags=["users"])
app.include_router(inventory_endP.router, tags=["inventories"])
app.include_router(product_endP.router, tags=["products"])
app.include_router(carts_endP.router, tags=["carts"])
app.include_router(orders_endP.router, tags=["orders"])
app.include_router(reports_endP.router, tags=["reports"])