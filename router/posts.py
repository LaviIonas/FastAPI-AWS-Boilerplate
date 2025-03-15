from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schemas
from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.CreatePost])
def test_posts(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()

    return  post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreatePost])
def test_posts_sent(post_post:schemas.CreatePost, db:Session = Depends(get_db)):

    new_post = models.Post(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return [new_post]