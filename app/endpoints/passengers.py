from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.passenger import Passenger
from app.schemas.passengers import (
    PassengerCreate,
    PassengerResponse,
    PassengerUpdate
)

router = APIRouter(prefix="/api/passengers", tags=["passengers"])


# CREAR
@router.post("", response_model=PassengerResponse, status_code=status.HTTP_201_CREATED)
async def create_passenger(
    payload: PassengerCreate,
    db: AsyncSession = Depends(get_db)
) -> Passenger:

    new_passenger = Passenger(**payload.model_dump())

    db.add(new_passenger)
    await db.commit()
    await db.refresh(new_passenger)

    return new_passenger


# LISTAR TODOS
@router.get("", response_model=list[PassengerResponse])
async def get_passengers(
    db: AsyncSession = Depends(get_db)
) -> list[Passenger]:

    result = await db.execute(select(Passenger))
    return list(result.scalars().all())


# LISTAR POR ID
@router.get("/{passenger_id}", response_model=PassengerResponse)
async def get_passenger(
    passenger_id: str,
    db: AsyncSession = Depends(get_db)
) -> Passenger:

    passenger = await db.get(Passenger, passenger_id)

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")

    return passenger


# ACTUALIZAR
@router.put("/{passenger_id}", response_model=PassengerResponse)
async def update_passenger(
    passenger_id: str,
    payload: PassengerUpdate,
    db: AsyncSession = Depends(get_db)
) -> Passenger:

    passenger = await db.get(Passenger, passenger_id)

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(passenger, key, value)

    await db.commit()
    await db.refresh(passenger)

    return passenger


# ELIMINAR
@router.delete("/{passenger_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_passenger(
    passenger_id: str,
    db: AsyncSession = Depends(get_db)
) -> None:

    passenger = await db.get(Passenger, passenger_id)

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")

    await db.delete(passenger)
    await db.commit()