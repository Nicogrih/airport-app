from fastapi import FastAPI
from app.endpoints.airlines import router as airline_router
from app.endpoints.airports import router as airport_router

app = FastAPI(title="airport-app")

app.include_router(airline_router)
app.include_router(airport_router)