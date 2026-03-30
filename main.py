from fastapi import FastAPI
from src.api import users, categories, locations, posts, comments
from src.infrastructure.sqlite.configSQL import Base, engine
from src.infrastructure.sqlite.models import UserModels, PostModels, LocationModels, CategoryModels, CommentModels # noqa

# Base.metadata.create_all(bind=engine) # После добавления alembic выполнение данной строки скорее всего не нужно.

app = FastAPI()


# Добавил роутеры, чтоб не импортировать последовательно один API в другой.
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)