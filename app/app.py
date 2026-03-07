from fastapi import FastAPI

# from app.endpoints.health import router as health_router
from app.endpoints.users import router as users_router
from app.endpoints.reservations import router as reservations_router
from app.endpoints.flights import router as flights_router
from app.endpoints.passengers import router as passengers_router

app = FastAPI(title="airport-app")

# app.include_router(health_router)
app.include_router(users_router)
app.include_router(reservations_router)
app.include_router(flights_router)
app.include_router(passengers_router)