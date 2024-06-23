from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import users
from app.database import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])   
