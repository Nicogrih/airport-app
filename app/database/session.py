import os
import urllib.parse

from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está definido en el archivo .env")

# Asegurar que la URL use asyncpg
if "asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# impiar parámetros no soportados por asyncpg (sslmode, channel_binding)
parsed = urllib.parse.urlparse(DATABASE_URL)
query_params = urllib.parse.parse_qsl(parsed.query)

# Filtrar parámetros no soportados
filtered_params = [
    (k, v) for k, v in query_params if k not in ("sslmode", "channel_binding")
]

# Reconstruir query string
new_query = urllib.parse.urlencode(filtered_params)

# Reconstruir URL
DATABASE_URL = urllib.parse.urlunparse(
    (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment,
    )
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"ssl": True},  # SSL habilitado para asyncpg
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
