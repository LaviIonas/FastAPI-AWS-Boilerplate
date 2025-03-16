from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    id: str
    title: str
    summary: str
    authors: List[str]
    link: str
    pdf_url: str

class SearchResults(BaseModel):
    results: List[SearchResult]

class PaperCreate(PaperBase):
    notes: Optional[str] = None

class PaperWithNotes(PaperBase):
    id: int
    notes: Optional[str] = None
    
    class Config:
        orm_mode = True

class NotesUpdate(BaseModel):
    notes: str