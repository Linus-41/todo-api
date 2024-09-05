from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.db import Base

user_todo_share_association = Table(
    'user_todo_share_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('todo_id', Integer, ForeignKey('todo.id'))
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    todos = relationship("ToDo", back_populates="owner")
    shared_todos = relationship(
        "ToDo",
        secondary=user_todo_share_association,
        back_populates="shared_with"
    )
    categories = relationship("Category", back_populates="owner")
