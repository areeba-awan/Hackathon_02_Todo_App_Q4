import asyncio
from backend.database.engine import engine
from backend.models.base import create_db_and_tables

# Import all models to register them with SQLModel metadata
from backend.models import user, todo

async def init_db():
    print("Initializing database...")
    await create_db_and_tables(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())