from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email:EmailStr
    password: str
    confirmPassword: str

class UserOut(BaseModel):
    name: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    name: str