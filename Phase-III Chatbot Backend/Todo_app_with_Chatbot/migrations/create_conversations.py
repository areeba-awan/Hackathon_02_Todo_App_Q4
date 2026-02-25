"""Database migration for conversation and message tables.

Run this script to create the necessary tables for chat history:
    python backend/migrations/create_conversations.py
"""
import sys
import os

# Add backend and models to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'models'))

from sqlmodel import SQLModel, create_engine
from conversation import Conversation, Message
from db import engine


def create_conversations_tables():
    """Create conversation and message tables."""
    print("Creating conversations table...")
    Conversation.__table__.create(engine)
    print("✓ conversations table created")
    
    print("Creating messages table...")
    Message.__table__.create(engine)
    print("✓ messages table created")
    
    print("\n✅ Migration complete! Chat history tables are ready.")


if __name__ == "__main__":
    try:
        create_conversations_tables()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nMake sure:")
        print("1. DATABASE_URL is set in .env file")
        print("2. Database connection is working")
        print("3. You have proper permissions")
        sys.exit(1)
