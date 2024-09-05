from pydantic import BaseModel

from app.schemas.category import Category
from app.schemas.todo import ToDo


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    todos: list[ToDo] = []
    categories: list[Category] = []
    shared_todos: list[ToDo] = []

    class Config:
        from_attributes = True


class ShareToDoRequest(BaseModel):
    user_id: int
