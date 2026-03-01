from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.users import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)) -> list[UserRead]:
    result = await db.execute(select(User).order_by(User.created_at.desc()))

    return list(result.scalars().all())


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    user = User(
        email=str(payload.email),
        full_name=payload.full_name,
        role=payload.role or "CLIENT",
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    await db.refresh(user)

    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID, payload: UserUpdate, db: AsyncSession = Depends(get_db)
) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if payload.email is not None:
        user.email = payload.email

    if payload.full_name is not None:
        user.full_name = payload.full_name

    if payload.role is not None:
        user.role = payload.role

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> None:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await db.delete(user)
    await db.commit()

    return None
