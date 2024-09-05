from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas.user
from app import schemas
from app.database.db import get_db
from app.database import user as database
from app.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=app.schemas.user.User)
def create_user(user: app.schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = database.get_user_by_username(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return database.create_user(db=db, user=user)


@router.get("/me", response_model=app.schemas.user.User)
def read_current_user(
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    return current_user
