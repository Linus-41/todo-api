from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    text: str | None = None
    is_done: bool = False
    position: int | None = None


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

    class Config:
        from_attributes = True
