import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.database.db import get_db
import app.database.user
import app.database.auth
from app.models.auth import Token
import app.schemas.auth
from app.security import ACCESS_TOKEN_EXPIRES, create_access_token, verify_password, create_refresh_token, SECRET_KEY, \
    ALGORITHM

router = APIRouter()


# Authenticate user by checking if he exists and if password is valid
def authenticate_user(db: Session, username: str, password: str):
    user = app.database.user.get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


# Route to authorize and get access token
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.user_name}, expires_delta=ACCESS_TOKEN_EXPIRES)
    refresh_token = create_refresh_token(data={"sub": user.user_name})

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
def refresh_access_token(token: app.schemas.auth.TokenRefresh, db: Session = Depends(get_db)):
    if app.database.auth.is_token_invalid(db, token.refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    try:
        payload = jwt.decode(token.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        user = app.database.user.get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        access_token = create_access_token(data={"sub": user.user_name}, expires_delta=ACCESS_TOKEN_EXPIRES)
        return Token(access_token=access_token, refresh_token=token.refresh_token, token_type="bearer")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


# Endpoint to invalidate a token
@router.post("/invalidate-token", response_model=dict)
def invalidate_token(
        token_invalidation: app.schemas.auth.TokenInvalidation,
        db: Session = Depends(get_db)
):
    token = token_invalidation.token

    try:
        # Decode the token to ensure it's valid
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Check if the user exists in the system
        user = app.database.user.get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if app.database.auth.is_token_invalid(db, token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Add the token to the invalid tokens list
        app.database.auth.add_invalid_token(db, token)

        return {"message": "Token has been invalidated successfully"}

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
