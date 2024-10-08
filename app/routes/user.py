from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import app.schemas.user
from app.database.db import get_db
import app.database.user
from app.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


# create new user
@router.post("/", response_model=app.schemas.user.User)
def create_user(user: app.schemas.user.UserCreate,
                response: Response,
                db: Session = Depends(get_db)):
    db_user = app.database.user.get_user_by_username(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    response.status_code = status.HTTP_201_CREATED
    return app.database.user.create_user(db=db, user=user)


# fetch current logged in user
@router.get("/me", response_model=app.schemas.user.User)
def read_current_user(
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    return current_user
