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
    # Validate category ownership
    if todo.category_id is not None:
        category = get_category(db, todo.category_id)
        if category is None or category.user_id != user_id:
            raise HTTPException(status_code=400, detail="Invalid category_id: Category does not belong to the user")

    if todo.position is None:
        max_position = db.query(models.ToDo.position).filter_by(owner_id=user_id).order_by(
            models.ToDo.position.desc()).first()
        todo.position = (max_position[0] + 1) if max_position else 1
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

    # Validate category ownership
    if todo.category_id is not None:
        category = get_category(db, todo.category_id)
        if category is None or category.user_id != db_todo.owner_id:
            raise HTTPException(status_code=400, detail="Invalid category_id: Category does not belong to the user")

    db_todo.title = todo.title
    db_todo.text = todo.text
    db_todo.is_done = todo.is_done
    db_todo.position = todo.position
    db_todo.category_id = todo.category_id
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def create_user_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    db_category = models.Category(**category.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()


def update_category(db: Session, category: schemas.CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.id == category.id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category was not found")
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category
