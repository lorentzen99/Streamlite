from fastapi import FastAPI
from app.api import users, items, products
from app.database import engine, SessionLocal

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(items.router, prefix="/items", tags=["items"])
