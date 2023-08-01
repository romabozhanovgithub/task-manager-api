from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from app.db.core import engine


async def get_session() -> AsyncIterator[SQLAlchemyAsyncSession]:
    async_session_local = SQLAlchemyAsyncSession(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session_local as async_session:
        async with async_session as session:
            try:
                session: SQLAlchemyAsyncSession
                yield session
            except Exception as e:
                print(e)
                await session.rollback()
                raise e


async def close_connection():
    await engine.dispose()
