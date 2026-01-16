from sqlmodel import Session
from contextlib import contextmanager
from typing import Generator
import logging

from .engine import engine

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Database session error: {e}")
        raise
    finally:
        session.close()

__all__ = ["get_session", "get_session_context"]