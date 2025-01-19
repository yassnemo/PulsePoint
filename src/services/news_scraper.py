import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_news(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.find('h1')
        
        # Get main content paragraphs
        paragraphs = soup.find_all('p')
        content_paragraphs = [p.get_text().strip() for p in paragraphs 
                            if p.get_text().strip() and 
                            not p.find_parent(class_=['metadata', 'footer', 'header'])]

                # Extract main image - target BBC's main article image
        image_url = None
        image_selectors = [
            'img[src*="ichef.bbci.co.uk"]',  # Target BBC's image domain
            'img[src*="news/1024"]',         # Target news images
            '.e1mo64ex0 img[src*="ichef"]',  # Main article image with ichef domain
            'img.ssrcss-evoj7m-Image[src*="ichef"]',  # Standard BBC image with ichef
            'picture source[srcset*="ichef"]'  # Picture element with ichef
        ]

        for selector in image_selectors:
            image = soup.select_one(selector)
            if image:
                # Try src attribute first
                if image.get('src') and 'ichef.bbci.co.uk' in image.get('src'):
                    image_url = image['src']
                    logger.debug(f"Found BBC image URL from src: {image_url}")
                    break
                # Try srcset attribute
                elif image.get('srcset') and 'ichef.bbci.co.uk' in image.get('srcset'):
                    srcset = image['srcset'].split(',')[0].strip().split(' ')[0]
                    image_url = srcset
                    logger.debug(f"Found BBC image URL from srcset: {image_url}")
                    break

        logger.debug(f"Final BBC image URL: {image_url}")

        return {
            'title': title.get_text().strip(),
            'content': ' '.join(content_paragraphs),
            'image': image_url
        }
        
    except Exception as e:
        logger.error(f"Error scraping article: {str(e)}")
        return None