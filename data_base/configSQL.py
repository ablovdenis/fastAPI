from sqlalchemy import create_engine

from .models.BaseModels import Base
from .models.CategoryModels import CategoryModel
from .models.UserModels import UserModel
from .models.PostModels import PostModel
from .models.LocationModels import LocationModel
from .models.CommentModels import CommentModel

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