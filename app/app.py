from fastapi import FastAPI

from app.endpoints.passengers import router as passengers_router
from app.endpoints.flights import router as flights_router

app = FastAPI()

app.include_router(passengers_router)
app.include_router(flights_router)