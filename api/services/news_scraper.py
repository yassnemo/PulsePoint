from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

logger = logging.getLogger(__name__)

@lru_cache(maxsize=100)
def scrape_author(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                java_script_enabled=True,
                ignore_https_errors=True
            )
            page = context.new_page()
            page.goto(url)
            
            # Wait and try multiple selectors
            selectors = [
                'span.sc-2b5e3b35-7.bZCrck',
                'div[data-testid="byline-new-contributors"] span',
                'span[class*="bZCrck"]'
            ]
            
            for selector in selectors:
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    author_span = page.query_selector(selector)
                    if author_span:
                        author_name = author_span.inner_text()
                        logger.debug(f"Found author with selector {selector}: {author_name}")
                        context.close()
                        browser.close()
                        return author_name
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {str(e)}")
                    continue
            
            logger.warning("No author found with any selector")
            context.close()
            browser.close()
            return "BBC News"
            
    except Exception as e:
        logger.error(f"Error scraping author: {str(e)}")
        return "BBC News"
def scrape_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')
        title_text = title.get_text().strip() if title else ""
        
        paragraphs = soup.find_all('p')
        content_paragraphs = [p.get_text().strip() for p in paragraphs 
                            if p.get_text().strip() and 
                            not p.find_parent(class_=['metadata', 'footer', 'header'])]
        
        image = soup.find('img', src=lambda x: x and 'ichef.bbci.co.uk' in x)
        image_url = image['src'] if image else None
        
        return {
            'title': title_text,
            'content': ' '.join(content_paragraphs),
            'image': image_url
        }
    except Exception as e:
        logger.error(f"Error scraping content: {str(e)}")
        return None

def scrape_news(url):
    try:
        with ThreadPoolExecutor() as executor:
            content_future = executor.submit(scrape_content, url)
            author_future = executor.submit(scrape_author, url)
            
            content_data = content_future.result()
            author_name = author_future.result()
            
            if not content_data:
                return None
                
            content_data['author'] = author_name
            return content_data
            
    except Exception as e:
        logger.error(f"Error in parallel scraping: {str(e)}")
        return None