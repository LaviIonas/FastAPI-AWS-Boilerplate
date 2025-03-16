from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

from router.posts import router as posts_router
from router.papers import router as papers_router
from router.user import router as user_router
from router.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router)
app.include_router(papers_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Research Paper Management API"}


