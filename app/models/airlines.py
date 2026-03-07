from sqlalchemy import String,DateTime
from app.database.session import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

class Airline(Base):
    __tablename__ = "airlines"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    code : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default= func.now(), nullable=False)





