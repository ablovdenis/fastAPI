from fastapi import FastAPI
import uvicorn
import asyncio
from src.infrastructure.postgre.models import (category_models,
                                              comment_models,
                                              location_models,
                                              post_models,
                                              user_models)
from src.api import users, categories, locations, posts, comments, auth
# from src.infrastructure.postgre.database import Base, engine

# Base.metadata.create_all(bind=engine) # После добавления alembic выполнение данной строки скорее всего не нужно.

app = FastAPI()


app.include_router(users.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(auth.router)

async def main() -> None:
    config = uvicorn.Config(
        "main:app", host="127.0.0.1", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    asyncio.run(main())