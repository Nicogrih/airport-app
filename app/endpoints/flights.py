from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.session import get_db
from app.models.flight import Flight
from app.schemas.flights import (
    FlightCreate,
    FlightResponse,
    FlightUpdate
)

router = APIRouter(prefix="/api/flights", tags=["flights"])

#CREAR
@router.post("/", response_model=FlightResponse)
async def create_flight(
    flight: FlightCreate,
    db: AsyncSession = Depends(get_db)
):
    new_flight = Flight(**flight.model_dump())

    db.add(new_flight)
    await db.commit()
    await db.refresh(new_flight)

    return new_flight

#LISTAR TODOS
@router.get("/", response_model=list[FlightResponse])
async def get_flights(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Flight))
    return result.scalars().all()

#LISTAR POR ID
@router.get("/{flight_id}", response_model=FlightResponse)
async def get_flight(flight_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Flight).where(Flight.id == flight_id)
    )
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    return flight

#ACTUALIZAR
@router.put("/{flight_id}", response_model=FlightResponse)
async def update_flight(
    flight_id: str,
    flight_data: FlightUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Flight).where(Flight.id == flight_id)
    )
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    for key, value in flight_data.model_dump(exclude_unset=True).items():
        setattr(flight, key, value)

    await db.commit()
    await db.refresh(flight)

    return flight

#ELIMINAR
@router.delete("/{flight_id}")
async def delete_flight(flight_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Flight).where(Flight.id == flight_id)
    )
    flight = result.scalar_one_or_none()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    await db.delete(flight)
    await db.commit()

    return {"message": "Flight deleted"}