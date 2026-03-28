"""Migracion inicial completa

Revision ID: 53c3ac11e09c
Revises:
Create Date: 2026-03-27 21:55:16.338737

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "53c3ac11e09c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. CREACIÓN DE TABLAS BASE
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column(
            "role", sa.String(length=16), server_default="CLIENT", nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "airlines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_table(
        "airports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=255), nullable=False),
        sa.Column("iata_code", sa.String(length=3), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("iata_code"),
    )

    # 2. TABLAS CON DEPENDENCIAS
    op.create_table(
        "flights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("airline_id", sa.Integer(), nullable=False),
        sa.Column("flight_number", sa.String(length=20), nullable=False),
        sa.Column("origin_airport_id", sa.Integer(), nullable=False),
        sa.Column("destination_airport_id", sa.Integer(), nullable=False),
        sa.Column("departure_at", sa.DateTime(), nullable=False),
        sa.Column("arrival_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["airline_id"],
            ["airlines.id"],
        ),
        sa.ForeignKeyConstraint(
            ["destination_airport_id"],
            ["airports.id"],
        ),
        sa.ForeignKeyConstraint(
            ["origin_airport_id"],
            ["airports.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "airline_id", "flight_number", "departure_at", name="uq_flight_departure"
        ),
    )

    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "status", sa.String(length=20), server_default="PENDING", nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "passengers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reservation_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("document_number", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reservation_flights",
        sa.Column("reservation_id", sa.Integer(), nullable=False),
        sa.Column("flight_id", sa.Integer(), nullable=False),
        sa.Column("segment_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["flight_id"],
            ["flights.id"],
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservations.id"],
        ),
        sa.PrimaryKeyConstraint("reservation_id", "flight_id"),
        sa.UniqueConstraint(
            "reservation_id", "flight_id", name="uq_reservation_flight"
        ),
        sa.UniqueConstraint(
            "reservation_id", "segment_order", name="uq_reservation_segment"
        ),
    )


def downgrade() -> None:
    op.drop_table("reservation_flights")
    op.drop_table("passengers")
    op.drop_table("reservations")
    op.drop_table("flights")
    op.drop_table("airports")
    op.drop_table("airlines")
    op.drop_table("users")
