import uuid

from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, func, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Flight(Base):
    __tablename__ = "flights"
    __table_args__ = (
        CheckConstraint("origin_airport_id <> destination_airport_id", name="chk_flights_airports_different"),
        CheckConstraint("arrival_at > departure_at", name="chk_flights_time_order"),
        UniqueConstraint("airline_id", "flight_number", "departure_at", name="uq_flight_departure"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    airline_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("airlines.id"), nullable=False)
    origin_airport_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("airports.id"), nullable=False)
    destination_airport_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("airports.id"), nullable=False)

    flight_number: Mapped[str] = mapped_column(Text, nullable=False)

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

    airline: Mapped["Airline"] = relationship()
    origin_airport: Mapped["Airport"] = relationship(foreign_keys=[origin_airport_id])
    destination_airport: Mapped["Airport"] = relationship(foreign_keys=[destination_airport_id])
