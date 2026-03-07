from sqlalchemy import Column,String,DateTime
from app.database.session import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class Airline(Base):
    __tablename__ = "airlines"

    id = Column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    code = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default= func.now(), nullable=False)





