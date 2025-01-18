import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_news(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get title from h1
        title = soup.find('h1')
        if not title:
            logger.error("Title not found")
            return None
            
        # Get main content paragraphs
        paragraphs = soup.find_all('p')
        if not paragraphs:
            logger.error("No paragraphs found")
            return None
            
        # Filter out non-article paragraphs
        content_paragraphs = [p.get_text().strip() for p in paragraphs 
                            if p.get_text().strip() and 
                            not p.find_parent(class_=['metadata', 'footer', 'header'])]
        
        if not content_paragraphs:
            logger.error("No content paragraphs found")
            return None
            
        return {
            'title': title.get_text().strip(),
            'content': ' '.join(content_paragraphs)
        }
        
    except Exception as e:
        logger.error(f"Error scraping article: {str(e)}")
        return None
