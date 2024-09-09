from pydantic import BaseModel


# model for OAuth2 access token
class Token(BaseModel):
    access_token: str
    token_type: str


# Token data containing username
class TokenData(BaseModel):
    username: str | None = None
