# app/database/seeder.py
import asyncio
import uuid

from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.models.airlines import Airline
from app.models.airports import Airport
from app.models.flights import Flight
from app.models.reservations import Reservation
from app.models.reservation_flights import ReservationFlight
from app.models.passengers import Passenger
from sqlalchemy import select
from datetime import datetime, timedelta


async def seed_users(db):
    """Crear usuarios de prueba si no existen"""
    users_data = [
        {"email": "admin@admin.com", "full_name": "Administrador", "role": "ADMIN"},
        {
            "email": "gjimenez@gmail.com",
            "full_name": "Gerardo Jiménez",
            "role": "ADMIN",
        },
        {"email": "angelgutierrez@correo.com", "full_name": "Angel", "role": "CLIENT"},
    ]

    for user_data in users_data:
        result = await db.execute(select(User).where(User.email == user_data["email"]))
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(
                id=uuid.uuid4(),
                email=user_data["email"],
                full_name=user_data["full_name"],
                role=user_data["role"],
            )
            db.add(new_user)
            print(f"Usuario {user_data['email']} creado")
        else:
            print(f"Usuario {user_data['email']} ya existe")

    await db.commit()


async def seed_airlines(db):
    """Crear aerolíneas de prueba si no existen"""
    airlines_data = [
        {"code": "AVA", "name": "Avianca", "country": "Colombia"},
        {"code": "LAT", "name": "LATAM Airlines", "country": "Chile"},
        {"code": "WJA", "name": "WestJet", "country": "Canadá"},
        {"code": "AAL", "name": "American Airlines", "country": "Estados Unidos"},
        {"code": "JBU", "name": "JetBlue", "country": "Estados Unidos"},
    ]

    for airline_data in airlines_data:
        result = await db.execute(
            select(Airline).where(Airline.code == airline_data["code"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            new_airline = Airline(
                id=uuid.uuid4(),
                code=airline_data["code"],
                name=airline_data["name"],
                country=airline_data["country"],
            )
            db.add(new_airline)
            print(f"Aerolínea {airline_data['name']} ({airline_data['code']}) creada")
        else:
            # Actualizar country si está vacío
            if not existing.country:
                existing.country = airline_data["country"]
                print(f"Aerolínea {airline_data['name']} actualizada con country")
            else:
                print(f"Aerolínea {airline_data['name']} ya existe")

    await db.commit()


async def seed_airports(db):
    """Crear aeropuertos de prueba si no existen"""
    airports_data = [
        {
            "code": "MDE",
            "name": "José María Córdova International Airport",
            "city": "Medellín",
            "country": "Colombia",
        },
        {
            "code": "CLO",
            "name": "Alfonso Bonilla Aragón International Airport",
            "city": "Cali",
            "country": "Colombia",
        },
        {
            "code": "BOG",
            "name": "El Dorado International Airport",
            "city": "Bogotá",
            "country": "Colombia",
        },
        {
            "code": "MIA",
            "name": "Miami International Airport",
            "city": "Miami",
            "country": "United States",
        },
        {
            "code": "JFK",
            "name": "John F. Kennedy International Airport",
            "city": "Nueva York",
            "country": "United States",
        },
    ]

    for airport_data in airports_data:
        result = await db.execute(
            select(Airport).where(Airport.code == airport_data["code"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            new_airport = Airport(
                id=uuid.uuid4(),
                code=airport_data["code"],
                name=airport_data["name"],
                city=airport_data["city"],
                country=airport_data["country"],
            )
            db.add(new_airport)
            print(f"Aeropuerto {airport_data['name']} ({airport_data['code']}) creado")
        else:
            # Actualizar city y country si están vacíos
            updated = False
            if not existing.city:
                existing.city = airport_data["city"]
                updated = True
            if not existing.country:
                existing.country = airport_data["country"]
                updated = True

            if updated:
                print(f"Aeropuerto {airport_data['name']} actualizado")
            else:
                print(f"Aeropuerto {airport_data['name']} ya existe")

    await db.commit()


async def seed_flights(db):
    """Crear vuelos de prueba con precios y fechas variadas"""

    # Mapeo de IDs para asegurar integridad referencial
    result_airlines = await db.execute(select(Airline))
    airlines_map = {a.code: a.id for a in result_airlines.scalars().all()}

    result_airports = await db.execute(select(Airport))
    airports_map = {ap.code: ap.id for ap in result_airports.scalars().all()}

    # Datos diversificados basados en la estructura del backup
    flights_data = [
        {
            "airline": "AVA",
            "number": "AVA101",
            "origin": "BOG",
            "dest": "MDE",
            "dep": "2026-03-28 07:00:00+00",
            "arr": "2026-03-28 08:00:00+00",
            "price": 185000,
        },
        {
            "airline": "LAT",
            "number": "LAT225",
            "origin": "MDE",
            "dest": "CLO",
            "dep": "2026-03-28 15:30:00+00",
            "arr": "2026-03-28 16:25:00+00",
            "price": 142000,
        },
        {
            "airline": "AAL",
            "number": "AAL450",
            "origin": "MIA",
            "dest": "JFK",
            "dep": "2026-04-01 10:00:00+00",
            "arr": "2026-04-01 13:15:00+00",
            "price": 850000,
        },
        {
            "airline": "AVA",
            "number": "AVA010",
            "origin": "BOG",
            "dest": "MIA",
            "dep": "2026-04-02 06:15:00+00",
            "arr": "2026-04-02 10:05:00+00",
            "price": 1250000,
        },
        {
            "airline": "JBU",
            "number": "JBU901",
            "origin": "JFK",
            "dest": "BOG",
            "dep": "2026-04-05 22:00:00+00",
            "arr": "2026-04-06 03:45:00+00",
            "price": 980000,
        },
        {
            "airline": "WJA",
            "number": "WJA552",
            "origin": "JFK",
            "dest": "MIA",
            "dep": "2026-04-10 12:00:00+00",
            "arr": "2026-04-10 15:10:00+00",
            "price": 320000,
        },
    ]

    for f in flights_data:
        dep_time = datetime.fromisoformat(f["dep"])
        airline_id = airlines_map.get(f["airline"])

        # Verificación de duplicados antes de insertar
        result = await db.execute(
            select(Flight).where(
                Flight.airline_id == airline_id,
                Flight.flight_number == f["number"],
                Flight.departure_at == dep_time,
            )
        )
        if not result.scalar_one_or_none():
            new_flight = Flight(
                id=uuid.uuid4(),
                airline_id=airline_id,
                flight_number=f["number"],
                origin_airport_id=airports_map.get(f["origin"]),
                destination_airport_id=airports_map.get(f["dest"]),
                departure_at=dep_time,
                arrival_at=datetime.fromisoformat(f["arr"]),
                price_cop=f["price"],
                status="SCHEDULED",
            )
            db.add(new_flight)
            print(f"Vuelo {f['number']} ({f['airline']}) creado: ${f['price']} COP")

    await db.commit()


async def run():
    async with AsyncSessionLocal() as db:
        print("Iniciando seed de datos...")
        await seed_users(db)
        await seed_airlines(db)
        await seed_airports(db)
        await seed_flights(db)
        print("Seeding completado")


if __name__ == "__main__":
    asyncio.run(run())
