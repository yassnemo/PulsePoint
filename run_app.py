
"""
Alternative startup script for PulsePoint on Windows
This script provides better Windows compatibility and error handling
"""

import os
import sys
import logging
from werkzeug.serving import WSGIRequestHandler

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the Flask app
from src.app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom request handler to avoid Windows socket issues
class WindowsRequestHandler(WSGIRequestHandler):
    def log_request(self, code='-', size='-'):
        # Reduce logging noise
        pass

if __name__ == '__main__':
    try:
        print("=" * 50)
        print("🔥 PulsePoint News Summarizer")
        print("=" * 50)
        print("Starting application...")
        print("Local URL: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run with Windows-optimized settings
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            threaded=True,
            use_reloader=False,  # Disable reloader to prevent Windows socket errors
            request_handler=WindowsRequestHandler
        )
        
    except KeyboardInterrupt:
        print("\n\nShutting down PulsePoint...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        sys.exit(1)
