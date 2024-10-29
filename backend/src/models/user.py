from pydantic import BaseModel

from src.models.enums import UserLevel


class UserCredentials(BaseModel):
    email: str
    password: str


class UserPresentation(BaseModel):
    name: str
    surname: str
    email: str
    user_level: str


class UserToCreate(BaseModel):
    name: str
    surname: str
    email: str
    user_level: UserLevel
    password: str


class UserFilters(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    user_level: str | None = None
