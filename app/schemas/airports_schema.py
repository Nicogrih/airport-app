from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class AirportBase(BaseModel):
    code:str
    name:str
    country:str

class AirportCreate(AirportBase):
    pass

class AirportUpdate(BaseModel):
    code : Optional[str] = None
    name : Optional[str] = None
    country : Optional[str] = None

class AirportResponse(AirportBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True