# README.md

# 📰 PulsePoint

> A modern Flask web application that transforms lengthy BBC news articles into concise, readable summaries using AI.


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
   ```

3. Run the application:
   ```
   python src/app.py
   ```

4. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Usage

- On the main page, enter the news topic you want to summarize.
- The application will scrape articles from BBC.com and provide a summarized version for you to read.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
