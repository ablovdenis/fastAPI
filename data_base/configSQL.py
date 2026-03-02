from sqlalchemy import create_engine
from .models import *
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Взял из Интернета. Нужно для того, чтоб не держать БД открытым тогда, когда не надо.
def get_db():
    DataBase = SessionLocal()
    try:
        yield DataBase
    finally:
        DataBase.close()