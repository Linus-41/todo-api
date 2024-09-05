from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import app.schemas.todo
import app.schemas.user
from app import schemas
from app.database.db import get_db
from app.database import todo as database
from app.dependencies import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=app.schemas.todo.ToDo)
def create_user_todo(
        todo: app.schemas.todo.ToDoCreate,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user)
):

    return database.create_user_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=list[app.schemas.todo.ToDo])
def read_user_todos(
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    todos = current_user.todos + current_user.shared_todos
    return todos


@router.delete("/{todo_id}")
def delete_user_todo(
        todo_id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user),

):
    if todo_id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    database.delete_todo(db, todo_id)
    response.status_code = status.HTTP_204_NO_CONTENT


@router.put("/", response_model=app.schemas.todo.ToDo)
def update_user_todo(
    todo: app.schemas.todo.ToDoUpdate,
    db: Session = Depends(get_db),
    current_user: app.schemas.user.User = Depends(get_current_user)
):
    if todo.id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    return database.update_todo(db, todo)


@router.patch("/{todo_id}/mark_done", response_model=app.schemas.todo.ToDo)
def mark_user_todo_done(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: app.schemas.user.User = Depends(get_current_user)
):
    if todo_id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    return database.mark_todo_done(db, todo_id)


@router.post("/{todo_id}/share", response_model=app.schemas.todo.ToDo)
def share_todo(
        todo_id: int,
        share_request: app.schemas.user.ShareToDoRequest,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user),
):
    db_todo = database.get_todo_by_id(db, todo_id)
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to share this ToDo")

    return database.share_todo_with_user(db, todo_id, share_request.user_id)
