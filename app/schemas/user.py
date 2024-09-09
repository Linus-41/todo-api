from pydantic import BaseModel

from app.schemas.category import Category
from app.schemas.todo import ToDo


class UserBase(BaseModel):
    user_name: str


# Schema to create a user
class UserCreate(UserBase):
    password: str


# Schema of complete user
class User(UserBase):
    id: int
    todos: list[ToDo] = []
    categories: list[Category] = []
    shared_todos: list[ToDo] = []

    class Config:
        from_attributes = True


# Schema to share a todo
class ShareToDoRequest(BaseModel):
    user_id: int
