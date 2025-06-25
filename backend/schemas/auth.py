from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    login: str
    password: str

class UserForToken(UserLogin):
    role: str
    email: EmailStr
    name: str
    id: int
    second_name: str
    class Config:
        from_attributes = True