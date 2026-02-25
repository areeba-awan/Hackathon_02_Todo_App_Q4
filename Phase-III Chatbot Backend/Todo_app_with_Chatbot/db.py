from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment - use SQLite for Hugging Face Spaces by default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# For Hugging Face Spaces, use a file-based SQLite database
if "SPACE_ID" in os.environ:
    DATABASE_URL = "sqlite:///./todo_app.db"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

def create_db_and_tables() -> None:
    """Create all database tables."""
    # Import all models to ensure tables are created
    from models import User, Task
    from conversation_models.conversation import Conversation, Message
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
