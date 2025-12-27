# Async DB connection
# database.py
# -------------------
# Async DB connection with pooling

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Set your database URL here (PostgreSQL recommended)
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/grac3ind3x"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session():
    """FastAPI dependency for async DB session"""
    async with AsyncSessionLocal() as session:
        yield session
