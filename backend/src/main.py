from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.database.db import create_db_and_tables
from src.logging import LogConfig
from src.main_router import router

dictConfig(LogConfig().model_dump())


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    await app.state.db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

origins = [
    settings.server_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
