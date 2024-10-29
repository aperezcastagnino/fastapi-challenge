from fastapi import APIRouter

from src.api.v1.controllers import users
from src.api.v1.webhooks import counters

v1_router = APIRouter()
v1_router.include_router(users.router, prefix="/users")
v1_router.include_router(counters.router, prefix="/webhooks")
