from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.db import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=schemas.ToDo)
def create_todo_for_user(
        todo: schemas.ToDoCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):

    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=list[schemas.ToDo])
def read_todos(
        current_user: schemas.User = Depends(get_current_user)
):
    return current_user.todos


@router.delete("/{todo_id}")
def delete_todo(
        todo_id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),

):
    if todo_id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    crud.delete_todo(db, todo_id)
    response.status_code = status.HTTP_204_NO_CONTENT
