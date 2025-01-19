import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import logging

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.error(f"Failed to download NLTK data: {str(e)}")

def summarize_news(article):
    try:
        if not article or 'content' not in article:
            logger.error("Invalid article data")
            return None

        # Tokenize into sentences
        sentences = sent_tokenize(article['content'])
        if len(sentences) < 1:
            logger.error("No sentences found in article")
            return None

        # Process text
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(article['content'].lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]

        # Calculate word frequency
        freq_dist = FreqDist(words)
        
        # Score sentences
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq_dist:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = freq_dist[word]
                    else:
                        sentence_scores[sentence] += freq_dist[word]

        if not sentence_scores:
            logger.error("No sentences scored")
            return None

        # Get top 3 sentences
        summary_sentences = sorted(
            sentence_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]

        # Combine sentences
        summary = ' '.join([s[0] for s in summary_sentences])
        
        logger.debug(f"Successfully created summary of length: {len(summary)}")
        
        return {
            'title': article['title'],
            'summary': summary
        }

    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        return None

if __name__ == '__main__':
    # Test the summarizer
    test_article = {
        'title': 'Test Article',
        'content': 'This is a test article. It contains multiple sentences. We want to summarize this content.'
    }
    print(summarize_news(test_article))