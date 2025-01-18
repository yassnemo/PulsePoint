import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_scrape():
    url = "https://www.bbc.com/news/articles/cgrnn8zxdego"
    
    try:
        # Request with headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        logger.debug(f"Requesting URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Print raw HTML
        logger.debug("Raw HTML first 1000 characters:")
        logger.debug(response.text[:1000])
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check title
        title = soup.find('h1')
        logger.debug(f"Title found: {title is not None}")
        if title:
            logger.debug(f"Title text: {title.get_text()}")
            
        # Check paragraphs
        paragraphs = soup.find_all('p')
        logger.debug(f"Paragraphs found: {len(paragraphs)}")
        
        if paragraphs:
            logger.debug("First paragraph text:")
            logger.debug(paragraphs[0].get_text())
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_scrape()