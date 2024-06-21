from pydantic import BaseModel
from typing import Optional

class BaseEntityBase(BaseModel):
    name: str
    description: Optional[str] = None

class BaseEntityCreate(BaseEntityBase):
    pass

class BaseEntityUpdate(BaseEntityBase):
    pass
