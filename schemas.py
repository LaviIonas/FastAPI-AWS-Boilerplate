from pydantic import BaseModel
from typing import List

class PostBase(BaseModel):
    content: str
    title: str
    
    class Config:
        orm_mode = True

class CreatePost(PostBase):
    class Config:
        orm_mode = True


class PaperBase(BaseModel):
    id: str
    title: str
    summary: str
    authors: List[str]
    categories: List[str]
    link: str
    pdf_url: str
