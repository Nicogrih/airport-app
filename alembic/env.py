from logging.config import fileConfig
import asyncio
import urllib.parse
import re

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from app.models.airlines import Airline
from app.models.airports import Airport
from app.models.flights import Flight
from app.models.passengers import Passenger
from app.models.reservation_flights import ReservationFlight
from app.models.reservations import Reservation
from app.models.user import User
from app.database.base import Base

from alembic import context
import os

# this is the Alembic Config object
config = context.config

# Sobrescribir la URL con variable de entorno si existe
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Correr migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Función auxiliar para ejecutar migraciones."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def clean_url_for_asyncpg(url: str) -> str:
    """Limpia la URL removiendo parámetros que asyncpg no soporta."""
    # Remover +asyncpg si ya existe (lo agregaremos nosotros)
    url = url.replace("postgresql+asyncpg://", "postgresql://")

    # Parsear la URL
    parsed = urllib.parse.urlparse(url)

    # Obtener query params como lista de tuplas para mantener compatibilidad
    query_list = urllib.parse.parse_qsl(parsed.query)

    # Filtrar parámetros no soportados por asyncpg
    filtered_query = [
        (k, v) for k, v in query_list if k not in ("sslmode", "channel_binding")
    ]

    # Reconstruir query string
    new_query = urllib.parse.urlencode(filtered_query)

    # Reconstruir URL completa
    new_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    # Agregar +asyncpg al scheme
    return new_url.replace("postgresql://", "postgresql+asyncpg://", 1)


async def run_migrations_online() -> None:
    """Correr migraciones en modo 'online' usando async."""
    # Obtener la URL de configuración
    raw_url = config.get_main_option("sqlalchemy.url")

    # Validate that the URL is not None
    if raw_url is None:
        raise ValueError("DATABASE_URL is not configured")

    # Limpiar URL para asyncpg
    db_url = clean_url_for_asyncpg(raw_url)

    # Crear engine async con SSL configurado correctamente
    connectable = create_async_engine(
        db_url,
        poolclass=pool.NullPool,
        connect_args={"ssl": True},  # SSL habilitado para asyncpg
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations():
    """Función principal que ejecuta las migraciones."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


# Ejecutar
run_migrations()
