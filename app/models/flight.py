from sqlalchemy import Column, Text, ForeignKey, TIMESTAMP, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database.session import Base

class Flight(Base):
    __tablename__ = "flights"

    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    airline_id = Column(
        UUID(as_uuid=True),
        ForeignKey("airlines.id", ondelete="RESTRICT"),
        nullable=False
    )

    flight_number = Column(Text, nullable=False)

    origin_airport_id = Column(
        UUID(as_uuid=True),
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False
    )

    destination_airport_id = Column(
        UUID(as_uuid=True),
        ForeignKey("airports.id", ondelete="RESTRICT"),
        nullable=False
    )

    departure_at = Column(TIMESTAMP(timezone=True), nullable=False)

    arrival_at = Column(TIMESTAMP(timezone=True), nullable=False)

    status = Column(Text, nullable=False, default="SCHEDULED")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

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