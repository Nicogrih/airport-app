from sqlalchemy import Column, Text, Date, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database.session import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    reservation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reservation.id", ondelete="CASCADE"),
        nullable=False
    )

    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    document_number = Column(Text, nullable=False)

    birth_date = Column(Date, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )