from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(user_name=user.user_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ToDo).offset(skip).limit(limit).all()


def create_user_todo(db: Session, todo: schemas.ToDoCreate, user_id: int):
    db_todo = models.ToDo(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo


def update_todo(db: Session, todo: schemas.ToDoUpdate):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo was not found")
    db_todo.title = todo.title
    db_todo.text = todo.text
    db_todo.is_done = todo.is_done
    db.commit()
    db.refresh(db_todo)
    return db_todo
