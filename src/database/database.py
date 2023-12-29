import asyncio
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text
from src.config import settings
from src.database.models import Base, User

user = settings.postgres_user
pwd = settings.postgres_password
host = settings.postgres_host
port = settings.postgres_port
db = settings.postgres_db

DATABASE_URL = f"postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{db}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def check_database_connection(session: AsyncSession):
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        connection_success = await check_database_connection(session)
        if connection_success:
            print("Database connection successful")
        else:
            print("Database connection failed")


if __name__ == '__main__':
    asyncio.run(create_db_and_tables())
