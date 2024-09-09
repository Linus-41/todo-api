from sqlalchemy.orm import Session

import app.models.user
import app.schemas.user
from app.security import get_password_hash


# fetch user by username
def get_user_by_username(db: Session, user_name: str):
    return db.query(app.models.user.User).filter(app.models.user.User.user_name == user_name).first()


# create new user
def create_user(db: Session, user: app.schemas.user.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = app.models.user.User(user_name=user.user_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
