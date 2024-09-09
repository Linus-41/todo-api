from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


# Schema for creating categories
class CategoryCreate(CategoryBase):
    pass


# Schema for updating categories
class CategoryUpdate(CategoryBase):
    id: int


# Schema for complete categories e.g. for fetching
class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
