# app/api/crud.py

from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic
from pydantic import BaseModel

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class CRUDGeneric(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, entity_id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == entity_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 10) -> list:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, entity_id: int, obj_in: UpdateSchemaType
    ) -> ModelType:
        db_obj = db.query(self.model).filter(self.model.id == entity_id).first()
        if db_obj:
            update_data = obj_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, entity_id: int) -> ModelType:
        db_obj = db.query(self.model).filter(self.model.id == entity_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
