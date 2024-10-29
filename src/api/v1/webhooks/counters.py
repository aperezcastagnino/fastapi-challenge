from typing import Any, List

from fastapi import APIRouter, status

from src.api.v1.services.counters import CountersSevice
from src.database.db import SessionDep
from src.models.counter import CounterPresentation

router = APIRouter(tags=["Webhooks"])


@router.get(
    "/counters",
    status_code=status.HTTP_200_OK,
    response_model=List[CounterPresentation],
)
def get_counters(session: SessionDep) -> Any:
    return CountersSevice.get_counters(session)
