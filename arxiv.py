import feedparser
from urllib.parse import urlencode

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

def fetch_arxiv_papers(search_query, start=0, max_results=10, sort_by="submittedDate", sort_order="descending"):
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
        results.append({
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "abstract": entry.summary,
            "link": entry.link
        })
    
    return results

# Example usage
# if __name__ == "__main__":
#     search_query = "cat:cs.AI AND ti:transformer"
#     papers = fetch_arxiv_papers(search_query, max_results=5)
#     for paper in papers:
#         print(f"Title: {paper['title']}")
#         print(f"Authors: {', '.join(paper['authors'])}")
#         print(f"Abstract: {paper['abstract']}")
#         print(f"Link: {paper['link']}")
#         print("-" * 40)

# Example usage
if __name__ == "__main__":
    # Example 1: Fetch by arXiv ID
    arxiv_id = "2411.18585"
    paper_by_arxiv_id = fetch_paper_by_id(arxiv_id)
    print(f"Result for arXiv ID '{arxiv_id}':", paper_by_arxiv_id)
    
    # Example 2: Fetch by DOI
    doi = "10.48550/arXiv.2411.18585"
    paper_by_doi = fetch_paper_by_id(doi)
    print(f"Result for DOI '{doi}':", paper_by_doi)