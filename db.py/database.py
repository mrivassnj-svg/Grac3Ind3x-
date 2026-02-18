import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# Load secure URL from .env (Pillar: Engine Security)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/grac3ind3x")

# --- HIGH PERFORMANCE ENGINE CONFIGURATION ---
engine = create_async_engine(
    DATABASE_URL,
    # Pillar: Engine (Scalability)
    poolclass=QueuePool,
    pool_size=20,           # Increased for high clinician concurrency
    max_overflow=40,        # Allows spike handling during crisis events
    pool_timeout=30,        # Prevents hanging requests
    pool_recycle=1800,      # Recycles connections every 30m to prevent stale sockets
    pool_pre_ping=True,     # Verifies connection health before use (Liveness check)
    
    # Pillar: Response (Speed)
    echo=False,             # Set to True only for deep debugging
    future=True,            # SQLAlchemy 2.0 standard
)

# --- SESSION FACTORY ---
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False, # Essential for async: keeps objects available after commit
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# --- DEPENDENCY INJECTION ---
async def get_db():
    """
    FastAPI Dependency for Async DB Sessions.
    Ensures safe session closure even if the request fails.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
