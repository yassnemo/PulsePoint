from flask import Flask, render_template, request, flash, redirect, url_for
from services.news_scraper import scrape_news
from services.summarizer import summarize_news
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']
    logger.debug(f"Attempting to scrape URL: {url}")
    
    try:
        articles = scrape_news(url)
        if not articles:
            logger.error("No articles returned from scraper")
            flash('Unable to process this BBC article. Please check the URL and try again.')
            return redirect(url_for('index'))
            
        logger.debug(f"Article scraped successfully: {articles['title']}")
        
        summaries = summarize_news(articles)
        if not summaries:
            logger.error("Summarization failed")
            flash('Failed to summarize the article. Please try again.')
            return redirect(url_for('index'))
            
        logger.debug("Article summarized successfully")
        return render_template('summary.html', summaries=summaries)
        
    except Exception as e:
        logger.error(f"Error processing article: {str(e)}")
        flash('An error occurred while processing the article.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)