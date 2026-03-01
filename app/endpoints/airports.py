from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database.database import SessionLocal, get_db
from models.airports_models import Airport
from schemas.airports_schema import AirportCreate, AirportResponse, AirportUpdate

router = APIRouter(
    prefix="/airports",
    tags=["Airports"]
)

#CREAR(POST)
@router.post("/",response_model=AirportResponse)
def crear_airport(airport:AirportCreate, db:Session=Depends(get_db)):

    existe = db.query(Airport).filter(Airport.code == airport.code).first()

    if existe:
        raise HTTPException(status_code=400, detail="El código del Aeropuerto ya existe")
    
    nuevo_airport = Airport(
        code = airport.code,
        name = airport.name,
        country = airport.country
    )

    db.add(nuevo_airport)
    db.commit()
    db.refresh(nuevo_airport)

    return nuevo_airport

#LISTAR(GET)
@router.get("/",response_model=list[AirportResponse])
def listar_airport(db:Session=Depends(get_db)):
    return db.query(Airport).all()

#LISTAR POR ID(GET)
@router.get("/{airport_id}",response_model=AirportResponse)
def obtener_airport(airport_id:uuid.UUID,db:Session=Depends(get_db)):
    
    airport = db.query(Airport).filter(Airport.id == airport_id).first()

    if not airport:
        raise HTTPException(status_code=404, detail="Airport no encontrado")
    
    return airport

#ACTUALIZAR(PUT)
@router.put("/{airport_id}",response_model=AirportResponse)
def actualizar_airport(airport_id:uuid.UUID, data:AirportUpdate,db:Session=Depends(get_db)):

    airport = db.query(Airport).filter(Airport.id == airport_id).first()

    if not airport:
        raise HTTPException(status_code=404, detail="Airport no encontrado")
    
    if data.code is not None:
        airport.code = data.code

    if data.name is not None:
        airport.name = data.name

    if data.country is not None:
        airport.country = data.country

    db.commit()
    db.refresh(airport)

    return airport

#ELIMINAR(DELETED)
@router.delete("/{airport_id}")
def eliminar_airport(airport_id: uuid.UUID, db: Session = Depends(get_db)):

    airport = db.query(Airport).filter(Airport.id == airport_id).first()

    if not airport:
        raise HTTPException(status_code=404, detail="Airport no encontrado")

    db.delete(airport)
    db.commit()

    return {"message": "Airport Eliminado"}
    