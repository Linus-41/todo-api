from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.db import Base
from app.models.user import user_todo_share_association


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
    shared_with = relationship(
        "User",
        secondary=user_todo_share_association,
        back_populates="shared_todos"
    )
    category = relationship("Category", back_populates="todos")
