import unittest
from newscover.newsapi import fetch_latest_news
import json
from datetime import datetime, timedelta, timezone
import os 

class Unit_Tests(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, 'test_secrets.json')

        with open(json_path) as f:
            self.api_key = json.load(f).get('api_key')

    def test1(self):
        with self.assertRaises(ValueError):
            fetch_latest_news(self.api_key, '')
    
    def test2(self):
        lookback_days = 1
        articles = fetch_latest_news(self.api_key, 'climate change', lookback_days=lookback_days)

        self.assertIsInstance(articles, list)

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=lookback_days)

        for article in articles:
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            self.assertTrue(start <= date <= end, 'Test failed')

    def test3(self):
        with self.assertRaises(ValueError):
            fetch_latest_news(self.api_key, '93!@')


if __name__ == '__main__':
    unittest.main()