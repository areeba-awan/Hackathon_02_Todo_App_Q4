from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment (supports both DATABASE_URL and NEON_DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL") or "sqlite:///./todo.db"

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
