from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserCreateInternal(UserBase):
    hashed_password: str    

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserUpdateInternal(UserBase):
    hashed_password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass