import uuid

from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    airline_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("airlines.id"),
        nullable=False
        )
    flight_number: Mapped[str] = mapped_column(Text, nullable=False)

    origin_airport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("airports.id"),
        nullable=False
    )
    destination_airport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("airports.id"),
        nullable=False
    )

    departure_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    arrival_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    status: Mapped[str] = mapped_column(Text, nullable=False, default="SCHEDULED")

    price_cop: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="150000"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
