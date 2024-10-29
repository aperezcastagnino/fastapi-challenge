from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, Query, Security, status

from src.api.v1.services.counters import CountersSevice
from src.api.v1.services.users import UsersService
from src.database.db import SessionDep
from src.models.token import Token
from src.models.user import UserCredentials, UserFilters, UserPresentation, UserToCreate
from src.security import AuthManager, RoleChecker

router = APIRouter(tags=["Users"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(
    credentials: UserCredentials,
    session: SessionDep,
) -> Any:
    user = UsersService.login(credentials, session)
    return AuthManager.generate_token(user)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
def create_user(
    user_data: UserToCreate,
    session: SessionDep,
) -> Any:
    CountersSevice.increment_counter(session, "create_user")
    user = UsersService.create(user_data, session)
    return AuthManager.generate_token(user)


@router.get(
    "/all", status_code=status.HTTP_200_OK, response_model=List[UserPresentation]
)
def list_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    filters: UserFilters = Depends(),
    _: None = Security(RoleChecker.check_user_admin),
) -> Any:
    CountersSevice.increment_counter(session, "list_users")
    return UsersService.get_all(session, offset, limit, filters)
