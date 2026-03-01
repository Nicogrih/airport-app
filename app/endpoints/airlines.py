from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database.database import SessionLocal, get_db
from models.airlines_models import Airline
from schemas.airlines_schema import AirlineCreate,AirlineResponse,AirlineUpdate

router = APIRouter(
    prefix="/airlines",
    tags=["Airlines"]
)

#CREAR
@router.post("/", response_model=AirlineResponse)
def crear_airline(airline:AirlineCreate, db:Session=Depends(get_db)):

    existe = db.query(Airline).filter(Airline.code == airline.code).first()
    if existe:
        raise HTTPException(status_code=400, detail="El código de la aerolinea ya existe")

    nueva_airline = Airline(
        code = airline.code,
        name = airline.name
    )

    db.add(nueva_airline)
    db.refresh()
    db.commit(nueva_airline)

    return nueva_airline

#LISTAR
@router.get("/", response_model = list[AirlineResponse])
def listar_airline(db:Session = Depends(get_db)):
    return db.query(Airline).all()

#LISTAR POR ID
@router.get("/{airline_id}",response_model=AirlineResponse)
def obtener_airline(airline_id: uuid.UUID, db:Session = Depends(get_db)):

    airline = db.query(Airline).filter(Airline.id == airline_id).first()

    if not airline:
        raise HTTPException(status_code=404, detail="Airline no encontrada")
    
    return airline

#ACTUALIZAR POR ID
@router.put("/{airline_id}",response_model=AirlineResponse)
def actualizar_airline(airline_id:uuid.UUID, data : AirlineUpdate,db:Session = Depends(get_db)):

    airline = db.query(Airline).filter(Airline.id == airline_id).first()

    if not airline:
        raise HTTPException(status_code=404, detail="Airline no encontrada")
    
    if data.code is not None:
        airline.code = data.code

    if data.name is not None:
        airline.name = data.name

    db.commit()
    db.refresh(airline)

    return airline

#ELIMINAR POR ID
@router.delete("/{airline_id}")
def eliminar_airline(airline_id: uuid.UUID, db: Session = Depends(get_db)):

    airline = db.query(Airline).filter(Airline.id == airline_id).first()

    if not airline:
        raise HTTPException(status_code=404, detail="Airline no encontrada")

    db.delete(airline)
    db.commit()

    return {"message": "Airline eliminada"}