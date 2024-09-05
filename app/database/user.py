from sqlalchemy.orm import Session

import app.models.user
import app.schemas.user
from app import schemas
from app.security import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(app.models.user.User).filter(app.models.user.User.id == user_id).first()


def get_user_by_username(db: Session, user_name: str):
    return db.query(app.models.user.User).filter(app.models.user.User.user_name == user_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(app.models.user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: app.schemas.user.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = app.models.user.User(user_name=user.user_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
