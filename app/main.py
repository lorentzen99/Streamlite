from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import users, products
from app.database import run_migrations


app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])   
app.include_router(products.router, prefix="/products", tags=["products"])   
