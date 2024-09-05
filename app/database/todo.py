from sqlalchemy.orm import Session
from fastapi import HTTPException

import app.models.todo
import app.models.user
import app.schemas.todo
from app import schemas
from app.database.category import get_category


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(app.models.todo.ToDo).offset(skip).limit(limit).all()


def create_user_todo(db: Session, todo: app.schemas.todo.ToDoCreate, user_id: int):
    # Validate category ownership
    if todo.category_id is not None:
        category = get_category(db, todo.category_id)
        if category is None or category.user_id != user_id:
            raise HTTPException(status_code=400, detail="Invalid category_id: Category does not belong to the user")

    if todo.position is None:
        max_position = db.query(app.models.todo.ToDo.position).filter_by(owner_id=user_id).order_by(
            app.models.todo.ToDo.position.desc()).first()
        todo.position = (max_position[0] + 1) if max_position else 1
    db_todo = app.models.todo.ToDo(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo


def update_todo(db: Session, todo: app.schemas.todo.ToDoUpdate):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo was not found")

    # Validate category ownership
    if todo.category_id is not None:
        category = get_category(db, todo.category_id)
        if category is None or category.user_id != db_todo.owner_id:
            raise HTTPException(status_code=400, detail="Invalid category_id: Category does not belong to the user")

    for key, value in todo.model_dump().items():
        if value is not None:
            setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def mark_todo_done(db: Session, todo_id: int):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()
    db_todo.is_done = True
    db.commit()
    db.refresh(db_todo)
    return db_todo


def share_todo_with_user(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()
    db_user = db.query(app.models.user.User).filter(app.models.user.User.id == user_id).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_todo in db_user.shared_todos:
        raise HTTPException(status_code=409, detail="Todo already shared!")

    db_user.shared_todos.append(db_todo)
    db.commit()
    return db_todo
