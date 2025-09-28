from contextlib import asynccontextmanager

from databases import Database
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.app.services import settings

DATABASE_URL = settings.DATABASE_URL
database = Database(DATABASE_URL)
# metadata = MetaData()

engine = create_async_engine(
    DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite+aiosqlite://"),
    connect_args={"check_same_thread": False},
    future=True,
)

Base = declarative_base()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await database.disconnect()
    await engine.dispose()
