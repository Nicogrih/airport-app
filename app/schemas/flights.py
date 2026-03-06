from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FlightBase(BaseModel):
    airline_id:UUID
    flight_number:str
    origin_airport_id: UUID
    destination_airport_id: UUID
    departure_at: datetime
    arrival_at: datetime
    status: str = "SCHEDULED"

class FlightCreate(FlightBase):
    pass

class FlightUpdate(BaseModel):
    flight_number: str | None = None
    departure_at: datetime | None = None
    arrival_at: datetime | None = None
    status: str | None = None

class FlightResponse(FlightBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True