from fastapi import FastAPI
from app.api.endpoints import users

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])