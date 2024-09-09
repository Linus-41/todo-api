from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException

import app.models.todo
import app.models.user
import app.schemas.todo
from app.database.category import get_category


# fetch todo by id
def get_todo_by_id(db: Session, todo_id: int):
    return db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()


# fetch all todos for user
# with options to filter for status and if shared todos should be excluded
# also options for pagination
def get_user_todos(
        owner_id: int,
        db: Session,
        exclude_done: Optional[bool] = False,
        exclude_shared: Optional[bool] = False,
        skip: int = 0,
        limit: int = 100,
):
    query = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.owner_id == owner_id)

    if exclude_done is True:
        query = query.filter(app.models.todo.ToDo.is_done != exclude_done)

    if exclude_shared is True:
        query = query.filter(~app.models.todo.ToDo.shared_with.any())

    todos = query.offset(skip).limit(limit).all()
    return todos


# create new todo for user
def create_user_todo(db: Session, todo: app.schemas.todo.ToDoCreate, user_id: int):
    # Validate category ownership
    if todo.category_id is not None:
        category = get_category(db, todo.category_id)
        if category is None or category.user_id != user_id:
            raise HTTPException(status_code=400, detail="Invalid category_id: Category does not belong to the user")

    db_todo = app.models.todo.ToDo(**todo.model_dump(), owner_id=user_id)

    max_position = db.query(app.models.todo.ToDo.position).filter_by(owner_id=user_id).order_by(
        app.models.todo.ToDo.position.desc()).first()
    db_todo.position = (max_position[0] + 1) if max_position else 1

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# delete specific todo by id
def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo


# update specific todo by id
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


# toggle status (done or not) of a specific todo
def toggle_todo_status(db: Session, todo_id: int):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()
    db_todo.is_done = not db_todo.is_done
    db.commit()
    db.refresh(db_todo)
    return db_todo


# create share relationship between a todo and the user it is shared to
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


# update todo position
# logic to keep all user todos valid also implemented here
# if a user changes the position of a todo, positions of all other todos get updated accordingly
def update_todo_position(db: Session, todo_id: int, new_position: int):
    db_todo = db.query(app.models.todo.ToDo).filter(app.models.todo.ToDo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    owner_id = db_todo.owner_id

    owner_todos = (
        db.query(app.models.todo.ToDo)
        .filter(app.models.todo.ToDo.owner_id == owner_id)
        .order_by(app.models.todo.ToDo.position)
        .all()
    )

    owner_todos.remove(db_todo)

    if new_position < 1:
        new_position = 1
    elif new_position > len(owner_todos) + 1:
        new_position = len(owner_todos) + 1

    owner_todos.insert(new_position - 1, db_todo)

    for idx, todo in enumerate(owner_todos):
        todo.position = idx + 1

    db.commit()
    db.refresh(db_todo)
    return db_todo
