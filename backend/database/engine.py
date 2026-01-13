from sqlmodel import create_engine
import os
from typing import Generator
from sqlalchemy import text
from sqlalchemy.pool import QueuePool

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

engine_args = {
    "echo": True,
    "pool_pre_ping": True,
}

# Only add pooling + ssl for Postgres (Neon)
if DATABASE_URL.startswith("postgresql"):
    engine_args.update({
        "poolclass": QueuePool,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 300,
        "connect_args": {"sslmode": "require"},
    })

engine = create_engine(DATABASE_URL, **engine_args)

def get_engine():
    return engine

def validate_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database connection validation failed: {e}")
        return False

__all__ = ["engine", "get_engine", "validate_database_connection"]
