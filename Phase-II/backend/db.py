from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

def create_db_and_tables() -> None:
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.
    
    Yields:
        Session: Database session
        
    Usage:
        @app.get("/api/tasks")
        def list_tasks(session: Session = Depends(get_session)):
            ...
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
