import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import time

class SearchEngine:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.cache = {}

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Perform a web search and return results.
        Uses a simple caching mechanism to avoid repeated requests.
        """
        # Check cache first
        cache_key = f"{query}_{max_results}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Using DuckDuckGo HTML
            url = f"https://html.duckduckgo.com/html/?q={query}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result')[:max_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    results.append({
                        'title': title_elem.text.strip(),
                        'url': title_elem['href'],
                        'snippet': snippet_elem.text.strip()
                    })
            
            # Cache the results
            self.cache[cache_key] = results
            return results

        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def fetch_content(self, url: str) -> str:
        """Fetch and extract main content from a webpage."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(['script', 'style']):
                script.decompose()
                
            # Get text content
            text = ' '.join(soup.stripped_strings)
            return text
        
        except Exception as e:
            print(f"Content fetch error for {url}: {str(e)}")
            return ""
