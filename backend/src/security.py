from datetime import datetime, timedelta
from typing import Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.config import settings
from src.database.db import SessionDep
from src.database.schema import User
from src.models.enums import UserLevel
from src.models.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class PasswordManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)


class AuthManager:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @classmethod
    def _create_access_token(cls, user: User) -> Tuple[str, datetime]:
        expires = datetime.now() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        token = jwt.encode(
            claims={"exp": expires, "user_id": str(user.id)},
            key=settings.jwt_signing_key,
            algorithm="HS256",
        )

        return token, expires

    @classmethod
    def generate_token(cls, user: User) -> Token:
        if user is not None:
            token, expires = cls._create_access_token(user)

        return Token(access_token=token, expires_at=expires)

    @classmethod
    def get_user_from_token(cls, token: Token, session: Session) -> User:
        try:
            payload = jwt.decode(
                token=token, key=settings.jwt_signing_key, algorithms="HS256"
            )
        except (JWTError, ValidationError):
            raise cls.credentials_exception

        user = session.query(User).filter_by(id=payload["user_id"]).first()
        return user


class RoleChecker:
    @classmethod
    def check_user_admin(cls, session: SessionDep, token: str = Depends(oauth2_scheme)):
        user = AuthManager.get_user_from_token(token, session)
        if user.user_level != UserLevel.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: admin role required",
            )
