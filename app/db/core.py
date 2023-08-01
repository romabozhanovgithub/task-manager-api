from sqlalchemy.ext.asyncio import create_async_engine

from app.core import settings

engine = create_async_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)
