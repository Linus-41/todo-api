from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import app.schemas.category
import app.schemas.user
from app import schemas
from app.database.db import get_db
from app.database import category as database
from app.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=app.schemas.category.Category)
def create_user_category(
        category: app.schemas.category.CategoryCreate,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    return database.create_user_category(db=db, category=category, user_id=current_user.id)


@router.get("/", response_model=list[app.schemas.category.Category])
def read_user_categories(
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    return current_user.categories


@router.delete("/{category_id}")
def delete_user_category(
        category_id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user),

):
    if category_id not in [category.id for category in current_user.categories]:
        raise HTTPException(status_code=404, detail="Category was not found")

    database.delete_category(db, category_id)
    response.status_code = status.HTTP_204_NO_CONTENT


@router.put("/")
def update_user_category(
        category: app.schemas.category.CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    if category.id not in [category.id for category in current_user.categories]:
        raise HTTPException(status_code=404, detail="Category was not found")

    return database.update_category(db, category)
