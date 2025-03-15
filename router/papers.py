from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
from schemas import *
from fastapi import APIRouter
from database import get_db
import httpx
import ast
import xml.etree.ElementTree as ET

router = APIRouter(
    prefix='/papers',
    tags=['Papers']
)

def parse_arxiv_response(xml_content):
    """Parse the XML response from arXiv"""
    # Parse XML
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        raise HTTPException(status_code=500, detail=f"XML parsing error: {str(e)}")
    
    results = []
    
    # XML namespaces used in arXiv response
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    # Find all entry elements
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        # Extract basic info
        id_elem = entry.find('.//{http://www.w3.org/2005/Atom}id').text if entry.find('.//{http://www.w3.org/2005/Atom}id') is not None else ""
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text.strip() if entry.find('.//{http://www.w3.org/2005/Atom}title') is not None else ""
        summary = entry.find('.//{http://www.w3.org/2005/Atom}summary').text.strip() if entry.find('.//{http://www.w3.org/2005/Atom}summary') is not None else ""
        
        # Extract authors
        authors = []
        for author in entry.findall('.//{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name'):
            authors.append(author.text)
        
        # Extract links
        link = ""
        pdf_url = ""
        for link_elem in entry.findall('.//{http://www.w3.org/2005/Atom}link'):
            rel = link_elem.get('rel')
            if rel == 'alternate':
                link = link_elem.get('href', "")
            elif rel == 'related' and link_elem.get('title') == 'pdf':
                pdf_url = link_elem.get('href', "")
        
        results.append({
            'id': id_elem,
            'title': title,
            'summary': summary,
            'authors': authors,
            'link': link,
            'pdf_url': pdf_url
        })
    
    return results

async def fetch_arxiv_papers_async(query: str, max_results: int = 3):
    """Fetch papers from arXiv API"""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                               detail="Error fetching data from arXiv")
        
        # Parse the XML response
        return parse_arxiv_response(response.text)

@router.post('/fetch_arxiv_query/', response_model=List[SearchResult])
async def fetch_arxiv_query_result(search_query: SearchQuery):
    query = search_query.query
    result = await fetch_arxiv_papers_async(query, max_results=3)
    
    search_results = []
    for item in result:
        search_result = SearchResult(
            id=item['id'],
            title=item['title'],
            summary=item['summary'],
            authors=item['authors'],
            link=item['link'],
            pdf_url=item['pdf_url']
        )
        search_results.append(search_result)
    
    return search_results
    