from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
import logging
import os
import sys

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import services
from api.services.news_scraper import scrape_news
from api.services.summarizer import summarize_news
from api.services.translator import TranslationService

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app with correct paths
app = Flask(__name__,
    template_folder='../templates',
    static_folder='../static'
)

app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')

# Initialize services
translation_service = TranslationService()

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
            return jsonify({'error': 'Unable to process article'}), 400
            
        summaries = summarize_news(articles)
        if not summaries:
            logger.error("Summarization failed")
            return jsonify({'error': 'Failed to summarize'}), 400
            
        summaries['image'] = articles.get('image')
        summaries['author'] = articles.get('author')
        logger.debug(f"Final summaries: {summaries}")
            
        return render_template('summary.html', summaries=summaries)
        
    except Exception as e:
        logger.error(f"Error processing article: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'language' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        text = data['text']
        target_lang = data['language'].lower()
        
        translated_text = translation_service.translate_text(text, target_lang)
        if not translated_text:
            return jsonify({'error': 'Translation failed'}), 500
            
        return jsonify({
            'success': True,
            'translated': translated_text
        })
        
    except Exception as e:
        logger.error(f"Translation route error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/theme', methods=['POST'])
def update_theme():
    try:
        data = request.json
        theme = data.get('theme')
        session['theme'] = theme
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("PulsePoint application is running at http://127.0.0.1:5000")
    # Use threaded mode and disable reloader on Windows to avoid socket errors
    app.run(
        host='127.0.0.1', 
        port=5000, 
        debug=True,
        threaded=True,
        use_reloader=False  # Disable auto-reloader to prevent Windows socket errors
    )