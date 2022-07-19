from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from config import AppSettings


def create_db_engine(config: AppSettings) -> Engine:
    return create_engine(config.DB_URL)


def create_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, autoflush=False)
