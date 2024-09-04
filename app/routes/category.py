from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.db import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=schemas.Category)
def create_category_for_user(
        category: schemas.CategoryCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_user_category(db=db, category=category, user_id=current_user.id)


@router.get("/", response_model=list[schemas.Category])
def read_categories(
        current_user: schemas.User = Depends(get_current_user)
):
    return current_user.categories


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),

):
    if category_id not in [category.id for category in current_user.categories]:
        raise HTTPException(status_code=404, detail="Category was not found")

    crud.delete_category(db, category_id)
    response.status_code = status.HTTP_204_NO_CONTENT


@router.put("/")
def update_category(
        category: schemas.CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    if category.id not in [category.id for category in current_user.categories]:
        raise HTTPException(status_code=404, detail="Category was not found")

    return crud.update_category(db, category)
