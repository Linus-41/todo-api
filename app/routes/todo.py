from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.db import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=schemas.ToDo)
def create_user_todo(
        todo: schemas.ToDoCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):

    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=list[schemas.ToDo])
def read_user_todos(
        current_user: schemas.User = Depends(get_current_user)
):
    todos = current_user.todos + current_user.shared_todos
    return todos


@router.delete("/{todo_id}")
def delete_user_todo(
        todo_id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),

):
    if todo_id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    crud.delete_todo(db, todo_id)
    response.status_code = status.HTTP_204_NO_CONTENT


@router.put("/", response_model=schemas.ToDo)
def update_user_todo(
    todo: schemas.ToDoUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if todo.id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    return crud.update_todo(db, todo)


@router.patch("/mark_done/{todo_id}", response_model=schemas.ToDo)
def mark_user_todo_done(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if todo_id not in [todo.id for todo in current_user.todos]:
        raise HTTPException(status_code=404, detail="Todo was not found")

    return crud.mark_todo_done(db, todo_id)


@router.post("/share", response_model=schemas.ToDo)
def share_todo(
        share_request: schemas.ShareToDoRequest,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),
):
    db_todo = crud.get_todo_by_id(db, share_request.todo_id)
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to share this ToDo")

    return crud.share_todo_with_user(db, share_request.todo_id, share_request.user_id)
