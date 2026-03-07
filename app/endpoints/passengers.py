from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.session import get_db
from app.models.passenger import Passenger
from app.schemas.passengers import (
    PassengerCreate,
    PassengerResponse,
    PassengerUpdate
)

router = APIRouter(prefix="/api/passengers", tags=["passengers"])

#CREAR
@router.post("", response_model=PassengerResponse)
async def create_passenger(
    passenger: PassengerCreate,
    db: AsyncSession = Depends(get_db)
):
    new_passenger = Passenger(**passenger.model_dump())

    db.add(new_passenger)
    await db.commit
    await db.refresh(new_passenger)

    return new_passenger

#LISTAR TODOS
@router.get("", response_model=list[PassengerResponse])
async def get_passengers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Passenger))
    return result.scalars().all()

#LISTAR POR ID
@router.get("/{passenger_id}", response_model=PassengerResponse)
async def get_passenger(passenger_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Passenger).where(Passenger.id == passenger_id)
    )
    passenger = result.scalar_one_or_none()

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
    return passenger

#ACTUALIZAR
@router.put("/{passenger_id}", response_model=PassengerResponse)
async def update_passenger(
    passenger_id: str,
    passenger_data: PassengerUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Passenger).where(Passenger.id == passenger_id)
    )
    passenger = result.scalar_one_or_none()

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
    for key, value in passenger_data.model_dump(exclude_unset=True).items():
        setattr(passenger, key, value)

    await db.commit()
    await db.refresh(passenger)

    return passenger

#ELIMINAR
@router.delete("/{passenger_id}")
async def delete_passenger(passenger_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Passenger).where(Passenger.id == passenger_id)
    )
    passenger = result.scalar_one_or_none()

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
    await db.delete(passenger)
    await db.commit()

    return {"message": "Passenger deleted"}