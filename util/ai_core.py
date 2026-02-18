from database.db import engine
from orm import Base
import asyncio

async def initialize_clinical_vault():
    """Pillar: Engine - Ensures schema integrity and WAL mode."""
    async with engine.begin() as conn:
        # Create all tables defined in orm.py
        await conn.run_sync(Base.metadata.create_all)
        # Enable High-Performance WAL mode for SQLite (if applicable)
        await conn.execute("PRAGMA journal_mode=WAL;")
    print("G.R.A.C.E. Clinical Vault: INITIALIZED")

if __name__ == "__main__":
    asyncio.run(initialize_clinical_vault())
