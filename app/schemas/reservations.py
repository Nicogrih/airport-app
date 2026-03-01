from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReservationCreate(BaseModel):
    user_id: UUID
    status: str | None = Field(
        default="HOLD", pattern="^(HOLD|CONFIRMED|CANCELLED|EXPIRED)$"
    )
    total_amount_cop: int | None = Field(default=0, ge=0)


class ReservationUpdate(BaseModel):
    user_id: UUID | None = None
    status: str | None = Field(
        default=None, pattern="^(HOLD|CONFIRMED|CANCELLED|EXPIRED)$"
    )
    total_amount_cop: int | None = Field(default=None, ge=0)


class ReservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: str
    total_amount_cop: int
    created_at: datetime
