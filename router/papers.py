from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schemas
from fastapi import APIRouter
from database import get_db

from arxiv import fetch_arxiv_papers

router = APIRouter(
    prefix='/papers',
    tags=['Papers']
)

@router.get('/fetch_arxiv_query/{query}', status_code=status.HTTP_200_OK)
def get_arxiv_query_result(query:str):

    result = fetch_arxiv_papers(query, max_results=3)
    print(result)
    