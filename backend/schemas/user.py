from typing import Optional

from pydantic import BaseModel, EmailStr

from backend.models import User


class UserBase(BaseModel):
    name: str
    email: EmailStr
    login: str

class UserRead(UserBase):
    id: int
    name: str
    login: str
    role: str
    second_name: str
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str
    second_name: str
    login: str

class UserAuthentication(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    second_name: Optional[str]
    password: Optional[str]
    login: Optional[str]

class UserReadTravelsDTO(UserRead):
    pass

class UserWithToken(BaseModel):
    access_token: str
    id: int




