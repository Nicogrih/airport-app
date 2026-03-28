"""Migracion inicial limpia

Revision ID: 53c3ac11e09c
Revises:
Create Date: 2026-03-27 21:55:16.338737

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "53c3ac11e09c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Creación limpia desde cero."""

    # NOTA: Solo incluimos CREATE y ALTER necesarios para el estado final.
    # No incluimos DROP de tablas que no existen en una BD limpia.

    # 1. Aseguramos restricciones únicas finales
    op.create_unique_constraint(
        "uq_flight_departure",
        "flights",
        ["airline_id", "flight_number", "departure_at"],
    )

    op.create_foreign_key(
        "fk_flights_origin", "flights", "airports", ["origin_airport_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_flights_destination",
        "flights",
        "airports",
        ["destination_airport_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_flights_airline", "flights", "airlines", ["airline_id"], ["id"]
    )

    op.create_foreign_key(
        "fk_passengers_reservation",
        "passengers",
        "reservations",
        ["reservation_id"],
        ["id"],
    )

    op.create_unique_constraint(
        "uq_reservation_flight", "reservation_flights", ["reservation_id", "flight_id"]
    )
    op.create_unique_constraint(
        "uq_reservation_segment",
        "reservation_flights",
        ["reservation_id", "segment_order"],
    )

    op.create_foreign_key(
        "fk_res_flights_res",
        "reservation_flights",
        "reservations",
        ["reservation_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_res_flights_flight", "reservation_flights", "flights", ["flight_id"], ["id"]
    )

    op.create_foreign_key(
        "fk_reservations_user", "reservations", "users", ["user_id"], ["id"]
    )

    # Ajuste de la columna role en users
    op.alter_column(
        "users",
        "role",
        existing_type=sa.TEXT(),
        type_=sa.String(length=16),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # En el video no haremos downgrade, pero dejamos la estructura básica.
    pass
