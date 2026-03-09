from fastapi import FastAPI

from app.endpoints.users import router as users_router
from app.endpoints.airlines import router as airlines_router
from app.endpoints.airports import router as airports_router
from app.endpoints.flights import router as flights_router
from app.endpoints.reservations import router as reservations_router
from app.endpoints.passengers import router as passengers_router
from app.endpoints.reservation_flights import router as reservation_flights_router

app = FastAPI(title="airport-app", version="0.1.0")

app.include_router(users_router)
app.include_router(airlines_router)
app.include_router(airports_router)
app.include_router(flights_router)
app.include_router(reservations_router)
app.include_router(passengers_router)
app.include_router(reservation_flights_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
