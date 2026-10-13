"""Подключение к БД. По умолчанию SQLite (запускается без установки),
для PostgreSQL задайте переменную окружения:
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/asuma
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./asuma.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Зависимость FastAPI: db: Session = Depends(get_db)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    import models  # noqa: F401  (регистрирует таблицы)
    Base.metadata.create_all(engine)
