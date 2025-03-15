from fastapi import FastAPI

from database import engine
from models import Base

from router.posts import router as posts_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

