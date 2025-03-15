from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schemas
from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix='/user',
    tags=['User']
)



