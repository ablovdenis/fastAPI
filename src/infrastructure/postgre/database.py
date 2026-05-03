from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.postgres_url

# Создаём синхронный движок с полезными параметрами.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,      # Проверяет соединение перед использованием (избегает ошибок «соединение закрыто»).
    pool_recycle=3600,       # Пересоздаёт соединения раз в час.
    echo=False,              # Можно включить в True для отладки SQL-запросов.
)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    DataBase = SessionLocal()
    try:
        yield DataBase
    finally:
        DataBase.close()