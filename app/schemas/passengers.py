from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

class PassengerBase(BaseModel):
    reservation_id: UUID
    first_name: str
    last_name: str
    document_number: str
    birth_date: date | None = None

class PassengerCreate(PassengerBase):
    pass

class PassengerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    document_number: str | None = None
    birth_date: date | None = None

class PassengerResponse(PassengerBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True