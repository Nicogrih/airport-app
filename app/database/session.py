from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.database.config import get_database_url

DATABASE_URL = get_database_url()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"ssl": "require"},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base declarativa para modelos SQLAlchemy."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def db_ping() -> bool:
    """
    Verifica conectividad básica contra la DB ejecutando SELECT 1.

    Returns:
        bool: True si la DB responde, False si falla.
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
