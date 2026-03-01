from fastapi import FastAPI
from app.endpoints.health import router as health_router
from app.endpoints.users import router as users_router
from app.endpoints.reservations import router as reservations_router

app = FastAPI(title="airport-app")

app.include_router(health_router)
app.include_router(users_router)
app.include_router(reservations_router)
