from pydantic import BaseModel, Field, validator


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Name of the product")
    description: str = Field(None, max_length=100, description="Description of the product")
    price: float = Field(..., gt=0, description="Price of the product")
    is_active: bool = Field(True, description="Whether the product is active or not")

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return v

    class Config:
        use_enum_values = True

    @classmethod
    def __declare_last__(cls):
        cls.__field_validators__ = {
            'name': cls.validate_name,
        }


class ProductUpdate(BaseModel):
    name: str = Field(None, min_length=3, description="Name of the product")
    description: str = Field(None, max_length=100, description="Description of the product")
    price: float = Field(None, gt=0, description="Price of the product")
    is_active: bool = Field(None, description="Whether the product is active or not")

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return v

    class Config:
        use_enum_values = True

    @classmethod
    def __declare_last__(cls):
        cls.__field_validators__ = {
            'name': cls.validate_name,
        }


class ProductOut(BaseModel):
    name: str
    description: str
    price: float
    is_active: bool

    class Config:
        use_enum_values = True


class ProductInDB(ProductOut):
    id: int

    class Config:
        use_enum_values = True