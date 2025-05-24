from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.db.models.base import BaseModel

DATABASE_URL = "sqlite+aiosqlite:///./naukri.db"

# Create the async engine
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# Initialize DB and create tables
async def init_models():
    # Ensure all models are imported before metadata.create_all

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
