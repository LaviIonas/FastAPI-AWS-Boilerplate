import feedparser
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

def fetch_paper_by_id(identifier):
    """
    Fetch a paper's metadata from arXiv using its arXiv ID or DOI.

    Args:
        identifier (str): The arXiv ID (e.g., "2203.12345") or DOI (e.g., "10.48550/arXiv.2203.12345").

    Returns:
        dict: A dictionary containing the paper's metadata (title, authors, abstract, link) or None if not found.
    """
    ARXIV_API = "http://export.arxiv.org/api/query"
    
    # If identifier is a DOI, extract the arXiv ID
    if identifier.startswith("10.48550/arXiv."):
        arxiv_id = identifier.split("arXiv.")[-1]
    else:
        arxiv_id = identifier  # Assume it's already an arXiv ID

    # Build query string for arXiv ID
    search_query = f"id:{arxiv_id}"
    query_params = {
        "search_query": search_query,
        "start": 0,
        "max_results": 1  # Only expecting one result
    }
    query_string = urlencode(query_params)
    url = f"{ARXIV_API}?{query_string}"
    
    # Fetch data
    response = feedparser.parse(url)
    
    # Parse result
    if response.entries:
        entry = response.entries[0]
        return {
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "abstract": entry.summary,
            "link": entry.link
        }
    else:
        return None

def fetch_arxiv_papers(search_query, start=0, max_results=3, sort_by="submittedDate", sort_order="descending"):
    """
    Fetch papers from the arXiv API based on the query parameters.
    
    Args:
        search_query (str): The search query string (e.g., "cat:cs.AI AND ti:transformer").
        start (int): The index of the first result (default is 0).
        max_results (int): Maximum number of results to fetch (default is 10, max is 200).
        sort_by (str): Sort criteria, can be "relevance", "lastUpdatedDate", or "submittedDate" (default is "submittedDate").
        sort_order (str): Sort order, either "ascending" or "descending" (default is "descending").
    
    Returns:
        list: A list of dictionaries containing paper metadata.
    """
    ARXIV_API = "http://export.arxiv.org/api/query"
    
    # Build query string using urlencode to handle special characters
    query_params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }
    query_string = urlencode(query_params)
    url = f"{ARXIV_API}?{query_string}"
    # Fetch data
    response = feedparser.parse(url)

    # Parse results
    results = []
    for entry in response.entries:

        # Seperate out links
        for link in entry.links:
            if link.rel == "alternate":  # The main arXiv page
                arxiv_link = link.href
            elif link.title == "pdf":  # The direct PDF link
                pdf_link = link.href

        results.append({
            "id":entry.id,
            "title": entry.title,
            "summary": entry.summary,
            "authors": [author.name for author in entry.authors],
            "link": arxiv_link,
            "pdf_url": pdf_link
        })
    
    return results

async def fetch_arxiv_papers_async(query: str, max_results: int = 3):
    """Fetch papers from arXiv API"""
    base_url = "http://export.arxiv.org/api/query"

    start=0
    max_results=1 
    sort_by="submittedDate"
    sort_order="descending"

    params = {
        "search_query": f"all:{query}",
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        print(response)
        print(type(response))
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, 
                               detail="Error fetching data from arXiv")
        # return parse_arxiv_response(response.text)
        return response.text


# Example usage
if __name__ == "__main__":
    search_query = "cat:cs.AI AND ti:transformer"
    papers = fetch_arxiv_papers(search_query, max_results=3)
    print(papers)
    # for paper in papers:
    #     print(f"Title: {paper['title']}")
    #     print(f"Authors: {', '.join(paper['authors'])}")
    #     print(f"Abstract: {paper['abstract']}")
    #     print(f"Link: {paper['link']}")
    #     print("-" * 40)
