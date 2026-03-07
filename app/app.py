from fastapi import FastAPI
<<<<<<< HEAD
from app.endpoints.airlines import router as airline_router
from app.endpoints.airports import router as airport_router

app = FastAPI(title="airport-app")

app.include_router(airline_router)
app.include_router(airport_router)
=======
from app.endpoints.health import router as health_router
from app.endpoints.users import router as users_router
from app.endpoints.reservations import router as reservations_router

app = FastAPI(title="airport-app")

app.include_router(health_router)
app.include_router(users_router)
app.include_router(reservations_router)
>>>>>>> feat-dev/users-reservations-vertical
