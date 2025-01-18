import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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
        
        # Updated BBC selectors based on current HTML structure
        title = soup.find('h1')  # BBC articles usually have a simple h1 tag
        if not title:
            logger.error("Title element not found")
            return None
            
        # Try multiple possible content selectors
        content_selectors = [
            'article[data-component="text-block"]',
            'div[data-component="text-block"]',
            'article',
            'main'
        ]
        
        content = None
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                break
                
        if not content:
            logger.error("Content not found with any selector")
            return None
            
        # Get all paragraphs from content
        paragraphs = content.find_all('p')
        if not paragraphs:
            logger.error("No paragraphs found")
            return None
            
        text_content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        logger.debug(f"Found {len(paragraphs)} paragraphs")
        logger.debug(f"Title: {title.get_text().strip()}")
        
        return {
            'title': title.get_text().strip(),
            'content': text_content
        }
        
    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        return None