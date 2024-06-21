from pydantic import BaseModel

# Schema for creating a user
class UserCreate(BaseModel):
    username: str
    email: str
    role: str

# Schema for updating a user
class UserUpdate(BaseModel):
    username: str
    email: str
    role: str

# Schema for user response (output)
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True
