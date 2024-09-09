from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import app.schemas.category
import app.schemas.user
from app.database.db import get_db
import app.database.category
from app.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


# create a category for the current user
@router.post("/", response_model=app.schemas.category.Category)
def create_user_category(
        category: app.schemas.category.CategoryCreate,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    return app.database.category.create_user_category(db=db, category=category, user_id=current_user.id)


# get all user categories
@router.get("/", response_model=list[app.schemas.category.Category])
def read_user_categories(
        current_user: app.schemas.user.User = Depends(get_current_user),
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    categories = app.database.category.get_user_categories(db, current_user.id, skip=skip, limit=limit)
    return categories


# delete a specific user category
@router.delete("/{category_id}")
def delete_user_category(
        category_id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user),

):
    if category_id not in [category.id for category in current_user.categories]:
        raise HTTPException(status_code=404, detail="Category was not found")

    app.database.category.delete_category(db, category_id)
    response.status_code = status.HTTP_204_NO_CONTENT


# update a user category
@router.put("/")
def update_user_category(
        category: app.schemas.category.CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: app.schemas.user.User = Depends(get_current_user)
):
    if category.id not in [category.id for category in current_user.categories]:
        raise HTTPException(status_code=404, detail="Category was not found")

    return app.database.category.update_category(db, category)
