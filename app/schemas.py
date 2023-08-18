from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    class config():
        orm_mode = True



class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    
    class config():
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None