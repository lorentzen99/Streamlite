from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Type, TypeVar, Generic
from pydantic import BaseModel

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class CRUDGeneric(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, entity_id: int) -> ModelType:
        try:
            result = await db.execute(select(self.model).filter(self.model.id == entity_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> list:
        try:
            result = await db.execute(select(self.model).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        try:
            db_obj = self.model(**obj_in.model_dump())
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def update(self, db: AsyncSession, entity_id: int, obj_in: UpdateSchemaType) -> ModelType:
        try:
            result = await db.execute(select(self.model).filter(self.model.id == entity_id))
            db_obj = result.scalars().first()
            if db_obj:
                update_data = obj_in.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(db_obj, key, value)
                await db.commit()
                await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def delete(self, db: AsyncSession, entity_id: int) -> Optional[ModelType]:
        try:
            result = await db.execute(select(self.model).filter(self.model.id == entity_id))
            db_obj = result.scalars().first()
            if db_obj:
                await db.delete(db_obj)
                await db.commit()
                return db_obj  # Return the deleted object or its ID as needed
            return None  # Return None if the object was not found
        except SQLAlchemyError as e:
            await db.rollback()
            raise e