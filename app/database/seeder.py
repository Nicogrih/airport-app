import asyncio
import uuid

from app.database.session import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select


async def run():
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(User).where(User.email == "admin@admin.com")
        )
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(
                id=uuid.uuid4(),
                email="admin@admin.com",
                full_name="Administrador",
                role="ADMIN"
            )
            db.add(new_user)
            await db.commit()
            print("Usuario admin creado")
        else:
            print("El usuario ya existe")


if __name__ == "__main__":
    asyncio.run(run())