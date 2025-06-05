# api/arxiv_fetcher.py
import requests
from bs4 import BeautifulSoup

def search_arxiv(query: str, max_results: int = 3):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance"
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "xml")

    entries = soup.find_all("entry")
    papers = []
    for entry in entries:
        papers.append({
            "title": entry.title.text.strip(),
            "summary": entry.summary.text.strip(),
            "link": entry.id.text.strip()
        })
    return papers
