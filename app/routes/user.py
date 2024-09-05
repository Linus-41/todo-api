from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
def read_current_user(
        current_user: schemas.User = Depends(get_current_user)
):
    return current_user
