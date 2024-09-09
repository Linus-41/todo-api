from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    text: str | None = None
    is_done: bool = False
    category_id: int | None = None


# Schema to create todos
class ToDoCreate(ToDoBase):
    pass


# Schema to update todos
class ToDoUpdate(ToDoBase):
    title: str | None = None
    id: int


# Schema for complete todos e.g. for fetching
class ToDo(ToDoBase):
    id: int
    owner_id: int
    position: int

    class Config:
        from_attributes = True


# Schema to update todo position
class ToDoUpdatePosition(BaseModel):
    new_position: int
