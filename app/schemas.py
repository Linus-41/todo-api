from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    id: int


class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class ToDoBase(BaseModel):
    title: str
    text: str | None = None
    is_done: bool = False
    position: int | None = None
    category_id: int | None = None


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(ToDoBase):
    id: int


class ToDo(ToDoBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    todos: list[ToDo] = []
    categories: list[Category] = []

    class Config:
        from_attributes = True
