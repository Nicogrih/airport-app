from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class AirlineBase(BaseModel):
    code:str
    name:str

#Para crear(POST)
class AirlineCreate(AirlineBase):
    pass

#Para responder(GET)
class AirlineResponse(AirlineBase):
    id : UUID
    created_at : datetime

    class config:
        from_attributes = True

#Para actualizar(PUT)
class AirlineUpdate(BaseModel):
    code : Optional[str] = None
    name : Optional[str] = None