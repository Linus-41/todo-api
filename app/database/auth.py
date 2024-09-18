from sqlalchemy.orm import Session

from app.models.auth import InvalidToken


# Check if token has been invalidated
def is_token_invalid(session: Session, token_key: str) -> bool:
    # Query the table to check if the token key exists
    return session.query(InvalidToken).filter_by(key=token_key).first() is not None


# Invalidate token
def add_invalid_token(db: Session, token: str):
    invalid_token = InvalidToken(key=token)
    db.add(invalid_token)
    db.commit()
