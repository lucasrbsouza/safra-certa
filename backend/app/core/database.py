from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


def make_engine(url: str | None = None):
    return create_engine(url or get_settings().database_url)


def make_session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Lazy globals — initialized on first import of get_db in production
_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = make_engine()
    return _engine


def _get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = make_session_factory(_get_engine())
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()
