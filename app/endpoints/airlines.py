from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.airlines import Airline
from app.schemas.airlines import AirlineCreate, AirlineResponse, AirlineUpdate

router = APIRouter(prefix="/api/airlines", tags=["airlines"])

@router.get("", response_model=list[AirlineResponse])
async def listar_airlines(
    db: AsyncSession = Depends(get_db)
) -> list[AirlineResponse]:
    result = await db.execute(select(Airline))
    return list(result.scalars().all())


@router.get("/{airline_id}", response_model=AirlineResponse)
async def obtener_airline(
    airline_id: UUID, db: AsyncSession = Depends(get_db)
) -> Airline:
    """Obtiene una aerolínea por su UUID."""
    airline = await db.get(Airline, airline_id)
    
    if not airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Airline no encontrada"
        )
    return airline


@router.post("", response_model=AirlineResponse, status_code=status.HTTP_201_CREATED)
async def crear_airline(
    payload: AirlineCreate, db: AsyncSession = Depends(get_db)
) -> Airline:
    """Crea una nueva aerolínea verificando que el código sea único."""
    # Verificar si ya existe el código
    result = await db.execute(select(Airline).filter(Airline.code == payload.code))
    existe = result.scalars().first()
    
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El código de la aerolinea ya existe"
        )

    nueva_airline = Airline(
        code=payload.code,
        name=payload.name
    )
    
    db.add(nueva_airline)
    await db.commit()
    await db.refresh(nueva_airline)
    return nueva_airline


@router.put("/{airline_id}", response_model=AirlineResponse)
async def actualizar_airline(
    airline_id: UUID, payload: AirlineUpdate, db: AsyncSession = Depends(get_db)
) -> Airline:
    """Actualiza una aerolínea existente."""
    airline = await db.get(Airline, airline_id)
    
    if not airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Airline no encontrada"
        )

    # Actualización parcial (solo campos enviados)
    if payload.code is not None:
        airline.code = payload.code
    if payload.name is not None:
        airline.name = payload.name

    await db.commit()
    await db.refresh(airline)
    return airline


@router.delete("/{airline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_airline(
    airline_id: UUID, db: AsyncSession = Depends(get_db)
) -> None:
    """Elimina una aerolínea."""
    airline = await db.get(Airline, airline_id)
    
    if not airline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Airline no encontrada"
        )

    await db.delete(airline)
    await db.commit()
    return None