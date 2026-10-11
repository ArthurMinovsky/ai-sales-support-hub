from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
from app.db.models import Base


@lru_cache
def get_engine():
    url = get_settings().database_url
    opts = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=opts, pool_pre_ping=True)


def init_db():
    Base.metadata.create_all(bind=get_engine())


def get_db():
    session = sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)()
    try:
        yield session
    finally:
        session.close()
