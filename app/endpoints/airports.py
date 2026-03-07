from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.airports import Airport
from app.schemas.airports import AirportCreate, AirportResponse, AirportUpdate

router = APIRouter(prefix="/api/airports", tags=["airports"])

# LISTAR (GET)
@router.get("", response_model=list[AirportResponse])
async def listar_airports(
    db: AsyncSession = Depends(get_db)
) -> list[Airport]:
    """Obtiene la lista de todos los aeropuertos."""
    result = await db.execute(select(Airport))
    return list(result.scalars().all())


# LISTAR POR ID (GET)
@router.get("/{airport_id}", response_model=AirportResponse)
async def obtener_airport(
    airport_id: UUID, db: AsyncSession = Depends(get_db)
) -> Airport:
    """Obtiene un aeropuerto específico por su UUID."""
    airport = await db.get(Airport, airport_id)
    
    if not airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Airport no encontrado"
        )
    return airport


# CREAR (POST)
@router.post("", response_model=AirportResponse, status_code=status.HTTP_201_CREATED)
async def crear_airport(
    payload: AirportCreate, db: AsyncSession = Depends(get_db)
) -> Airport:
    """Crea un nuevo aeropuerto verificando que el código sea único."""
    # Verificar existencia previa por código
    result = await db.execute(select(Airport).filter(Airport.code == payload.code))
    existe = result.scalars().first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El código del Aeropuerto ya existe"
        )
    
    nuevo_airport = Airport(
        code=payload.code,
        name=payload.name,
        country=payload.country
    )

    db.add(nuevo_airport)
    await db.commit()
    await db.refresh(nuevo_airport)
    return nuevo_airport


# ACTUALIZAR (PUT)
@router.put("/{airport_id}", response_model=AirportResponse)
async def actualizar_airport(
    airport_id: UUID, payload: AirportUpdate, db: AsyncSession = Depends(get_db)
) -> Airport:
    """Actualiza los datos de un aeropuerto existente."""
    airport = await db.get(Airport, airport_id)

    if not airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Airport no encontrado"
        )
    
    # Actualización parcial
    if payload.code is not None:
        airport.code = payload.code
    if payload.name is not None:
        airport.name = payload.name
    if payload.country is not None:
        airport.country = payload.country

    await db.commit()
    await db.refresh(airport)
    return airport


# ELIMINAR (DELETE)
@router.delete("/{airport_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_airport(
    airport_id: UUID, db: AsyncSession = Depends(get_db)
) -> None:
    """Elimina un aeropuerto de la base de datos."""
    airport = await db.get(Airport, airport_id)

    if not airport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Airport no encontrado"
        )

    await db.delete(airport)
    await db.commit()
    return None
    