from pydantic import BaseModel
from sqlalchemy import Column, String

from app.database.db import Base


# model for persisting invalid but active tokens
class InvalidToken(Base):
    __tablename__ = "invalid_tokens"

    key = Column(String, primary_key=True)


# model for OAuth2 access token
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


# Token data containing username
class TokenData(BaseModel):
    username: str | None = None
