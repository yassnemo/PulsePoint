import unittest
from src.app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'News Summarizer', response.data)

    def test_summary_page(self):
        response = self.app.post('/summarize', data={'url': 'https://www.bbc.com/news'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Summary', response.data)

if __name__ == '__main__':
    unittest.main()