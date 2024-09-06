from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.models.category
import app.schemas.category
from app import schemas


def get_category(db: Session, category_id: int):
    return db.query(app.models.category).filter(app.models.category.id == category_id).first()


def get_user_categories(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
):
    query = db.query(app.models.category.Category).filter(app.models.category.Category.user_id == user_id)

    todos = query.offset(skip).limit(limit).all()
    return todos

def create_user_category(db: Session, category: app.schemas.category.CategoryCreate, user_id: int):
    db_category = app.models.category.Category(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    category = db.query(app.models.category.Category).filter(app.models.category.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()


def update_category(db: Session, category: app.schemas.category.CategoryUpdate):
    db_category = db.query(app.models.category.Category).filter(app.models.category.Category.id == category.id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category was not found")
    for key, value in category.model_dump().items():
        if value is not None:
            setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category
