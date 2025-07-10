# README.md

# 📰 PulsePoint

> Is a Flask web application that transforms lengthy BBC news articles into concise, readable summaries using AI.

![Light Mode](public/image-snippet.png)

## Project Structure

```
flask-news-app
├── src
│   ├── app.py                # entry point
│   ├── templates            
│   │   ├── base.html         # main template
│   │   ├── index.html        # for user input
│   │   └── summary.html      # displaying summarized news
│   ├── static                
│   │   ├── css
│   │   │   └── styles.css    # CSS styles 
│   │   └── js
│   │       └── main.js       # client-side interactions
│   └── services              
│       ├── news_scraper.py   # scrape news articles
│       └── summarizer.py     # summarize articles
├── tests                    
│   └── test_app.py           # to ensure functionality
├── requirements.txt        
└── README.md                 # Documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-news-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   playwright install chromium
   ```

3. Run the application:
   ```
   # Option 1: Direct execution
   python src/app.py
   
   # Option 2: Windows-optimized startup (recommended for Windows)
   python run_app.py
   ```

4. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

![Dark Mode](public/darkmode-image.png)

## Usage

- On the main page, enter the news topic you want to summarize.
- The application will scrape articles from BBC.com and provide a summarized version for you to read.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
