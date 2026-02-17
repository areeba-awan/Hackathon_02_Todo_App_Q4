from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from typing import AsyncGenerator
import uuid
from datetime import datetime
from sqlmodel import Field


def generate_uuid():
    """Generate a UUID4 string"""
    return str(uuid.uuid4())


class TimestampMixin:
    """Mixin class to add created_at and updated_at fields to models"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UUIDModel:
    """Mixin class to add id field to models"""
    id: str = Field(default_factory=generate_uuid, primary_key=True)


async def create_db_and_tables(engine):
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)