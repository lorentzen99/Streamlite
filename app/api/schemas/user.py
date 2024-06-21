from pydantic import BaseModel, EmailStr, Field, validator
import re

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str = Field(..., min_length=6, description="Username must be at least 6 characters long and contain only letters and numbers")
    first_name: str = Field(..., max_length=50, description="First name of the user")
    middle_name: str = Field(None, max_length=50, description="Middle name of the user")
    last_name: str = Field(..., max_length=50, description="Last name of the user")
    full_name: str = Field(..., max_length=100, description="Full name of the user")
    hashed_password: str = Field(..., min_length=8, description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character")
    email: EmailStr = Field(..., description="Email address of the user")
    phone: str = Field(None, max_length=11, description="Phone number of the user")
    role: str = Field(..., pattern=r'^(admin|user)$', description="Role of the user")
    is_admin: bool = Field(False, description="Whether the user is an admin or not")
    is_active: bool = Field(True, description="Whether the user is active or not")

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 6 or not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('Username must be at least 6 characters long and contain only letters and numbers')
        return v

    @validator('email')
    def email_no_whitespace(cls, v):
        if any(char.isspace() for char in v):
            raise ValueError('Whitespace is not allowed in email')
        return v

    @validator('hashed_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', v):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
        return v

    class Config:
        use_enum_values = True

    @classmethod
    def __declare_last__(cls):
        cls.__field_validators__ = {
            'username': cls.validate_username,
            'email': cls.email_no_whitespace,
            'hashed_password': cls.validate_password,
        }

# Schema for updating a user
class UserUpdate(BaseModel):
    username: str = Field(None, min_length=6, description="Username must be at least 6 characters long and contain only letters and numbers")
    first_name: str = Field(None, max_length=50, description="First name of the user")
    middle_name: str = Field(None, max_length=50, description="Middle name of the user")
    last_name: str = Field(None, max_length=50, description="Last name of the user")
    full_name: str = Field(None, max_length=100, description="Full name of the user")
    hashed_password: str = Field(None, min_length=8, description="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character")
    email: EmailStr = Field(None, description="Email address of the user")
    phone: str = Field(None, max_length=11, description="Phone number of the user")
    role: str = Field(None, pattern=r'^(admin|user)$', description="Role of the user")
    is_admin: bool = Field(None, description="Whether the user is an admin or not")
    is_active: bool = Field(None, description="Whether the user is active or not")

    class Config:
        use_enum_values = True

# Schema for user response (output)
class UserOut(BaseModel):
    username: str
    first_name: str
    middle_name: str = None
    last_name: str
    full_name: str
    email: EmailStr
    phone: str = None
    role: str
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True

# Schema for user stored in DB
class UserInDB(UserCreate):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True
