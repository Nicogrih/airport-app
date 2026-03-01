from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.database.session import db_ping

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
async def health() -> dict:
    return {"status": "ok"}


@router.get("/db")
async def health_db():
    ok = await db_ping()
    if not ok:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "error", "message": "Database connection failed"},
        )
    return {"database": "ok"}
