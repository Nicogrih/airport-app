from sqlalchemy import Column, Text, text, DateTime, Date, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.session import Base

class Passenger(Base):
    __tablename__ = "passengers"

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

    reservation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)

    document_number: Mapped[str] = mapped_column(Text, nullable=False)

    birth_date: Mapped[datetime]= mapped_column(DateTime(timezone=True), nullable=False)