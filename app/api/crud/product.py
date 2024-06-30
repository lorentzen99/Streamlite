from sqlalchemy.orm import Session
from app.api.models.product import Product
from app.api.schemas.product import ProductCreate, ProductUpdate
from app.api.crud.crud import CRUDGeneric


class CRUDProduct(CRUDGeneric[Product, ProductCreate, ProductUpdate]):
    def __init__(self, model: Product):
        super().__init__(model)

    def get(self, db: Session, product_id: int) -> Product:
        return super().get(db, product_id)

    def get_by_name(self, db: Session, name: str) -> Product:
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 10) -> list:
        return super().get_multi(db, skip, limit)
    
    def create(self, db: Session, product: ProductCreate) -> Product:
        return super().create(db, product)
    
    def update(self, db: Session, product_id: int, product: ProductUpdate) -> Product:
        return super().update(db, product_id, product)
    
    def delete(self, db: Session, product_id: int) -> Product:
        return super().delete(db, product_id)


crud_product = CRUDProduct(Product)
