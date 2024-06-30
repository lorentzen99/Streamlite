from sqlalchemy import Boolean, Column, Float, Integer, String
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}>"