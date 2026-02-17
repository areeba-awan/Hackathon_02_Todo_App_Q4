from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from backend.config.settings import settings
import os


# Create async engine
# For SQLite, we need to use the async dialect
if settings.DATABASE_URL.startswith("sqlite"):
    # For SQLite, we need to handle the path correctly
    db_url = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    db_url = settings.DATABASE_URL

engine = create_async_engine(
    db_url,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    pool_timeout=30,
)