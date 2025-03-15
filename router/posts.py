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