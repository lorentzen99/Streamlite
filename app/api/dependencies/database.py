from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal

# Dependency to get a database session
async def get_async_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
