from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.api.crud.product import crud_product
from app.api.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.api.dependencies.database import get_async_db


router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_async_db)]


@router.get("/", response_model=List[ProductOut])
async def read_products(db: db_dependency, skip: int = 0, limit: int = 10):
    return await crud_product.get_multi(db=db, skip=skip, limit=limit)

@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, db: db_dependency):
    return await crud_product.create(db=db, product=product)

@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int, db: db_dependency):
    db_product = await crud_product.get(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductUpdate, db: db_dependency):
    db_product = await crud_product.update(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", response_model=ProductOut)
async def delete_product(product_id: int, db: db_dependency):
    db_product = await crud_product.delete(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product