from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    todos = relationship("ToDo", back_populates="category", cascade="all, delete-orphan")
    owner = relationship("User", back_populates="categories")
