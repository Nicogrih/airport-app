from sqlalchemy import Column, Text, text, DateTime, ForeignKey, TIMESTAMP, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid

from app.database.session import Base

class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    airline_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("airlines.id", ondelete="RESTRICT"),
        nullable=False
    )

    flight_number: Mapped[str] = mapped_column(Text, nullable=False)

    origin_airport_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False
    )

    destination_airport_id: Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True),
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False
    )

    departure_at: Mapped[datetime]= mapped_column(DateTime(timezone=True), nullable=False)

    arrival_at: Mapped[datetime]= mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[str] = mapped_column(Text, nullable=False, default="SCHEDULED")

    

    __table_args__ = (
        CheckConstraint(
            "origin_airport_id <> destination_airport_id",
            name="chk_flights_airports_different"
        ),
        CheckConstraint(
            "arrival_at > departure_at",
            name="chk_flights_time_order"
        ),
        UniqueConstraint(
            "airline_id",
            "flight_number",
            "departure_at"
        ),
    )