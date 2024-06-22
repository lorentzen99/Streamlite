from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.auth import get_current_active_user
from app.api.crud.user import crud_user
from app.api.models.user import User
from app.api.schemas.user import UserCreate, UserUpdate, UserOut
from app.api.dependencies.database import get_async_db  # Assume this is the async version of get_db


router = APIRouter()

@router.get("/", response_model=List[UserOut])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    return await crud_user.get_multi(db=db, skip=skip, limit=limit)

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud_user.create(db=db, user=user)

@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud_user.get(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud_user.update(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=UserOut)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud_user.delete(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]