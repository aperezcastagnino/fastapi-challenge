from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select

from src.database.schema import User
from src.models.user import UserCredentials, UserFilters, UserPresentation, UserToCreate
from src.security import PasswordManager


class UsersService:
    def _apply_filters(filters: UserFilters, query: select) -> select:
        if filters is None:
            return query
        if filters.name:
            query = query.where(User.name == filters.name)
        if filters.surname:
            query = query.where(User.surname == filters.surname)
        if filters.email:
            query = query.where(User.email == filters.email)
        if filters.user_level:
            query = query.where(User.user_level == filters.user_level)
        return query

    @staticmethod
    def get_all(
        session: Session, offset: int, limit: int, filters: UserFilters | None = None
    ) -> List[UserPresentation]:
        query = select(User).offset(offset).limit(limit)
        query = UsersService._apply_filters(filters, query)

        users = session.execute(query).scalars().all()

        return [
            UserPresentation(
                name=user.name,
                surname=user.surname,
                email=user.email,
                user_level=user.user_level,
            )
            for user in users
        ]

    @staticmethod
    def create(user_to_create: UserToCreate, session: Session) -> User:
        user_existed = session.query(User).filter_by(email=user_to_create.email).first()
        if user_existed:
            raise HTTPException(409, "Email address already in use")

        hashed_password = PasswordManager.get_password_hash(user_to_create.password)

        user = User(
            name=user_to_create.name,
            surname=user_to_create.surname,
            email=user_to_create.email,
            user_level=user_to_create.user_level,
            password=hashed_password,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def login(credentials: UserCredentials, session: Session) -> User:
        login_exception = HTTPException(401, "Invalid email or password")

        user = session.query(User).filter_by(email=credentials.email).first()

        if not user:
            raise login_exception
        if not PasswordManager.verify_password(credentials.password, user.password):
            raise login_exception

        return user
