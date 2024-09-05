from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    text: str | None = None
    is_done: bool = False
    position: int | None = None
    category_id: int | None = None


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(ToDoBase):
    title: str | None = None
    id: int


class ToDo(ToDoBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
