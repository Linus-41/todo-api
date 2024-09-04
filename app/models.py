from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db import Base


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    todos = relationship("ToDo", back_populates="owner")
    categories = relationship("Category", back_populates="owner")
    

class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    text = Column(String, index=True, nullable=True)
    is_done = Column(Boolean, default=False)
    position = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)

    owner = relationship("User", back_populates="todos")
    category = relationship("Category", back_populates="todos")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    todos = relationship("ToDo", back_populates="category", cascade="all, delete-orphan")
    owner = relationship("User", back_populates="categories")
