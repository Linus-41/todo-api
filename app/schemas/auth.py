from pydantic import BaseModel


class TokenInvalidation(BaseModel):
    token: str


class TokenRefresh(BaseModel):
    refresh_token: str
