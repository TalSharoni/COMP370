import requests
from datetime import datetime, timedelta, timezone

def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    URL = 'https://newsapi.org/v2/everything'

    if news_keywords == '':
        raise ValueError("Keyword must be provided")
    if not news_keywords.replace(" ", "").isalpha():
        raise ValueError('Invalid keyword provided - must be alphabetic characters')

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=lookback_days)
    end = end.strftime('%Y-%m-%dT%H:%M:%SZ')
    start = start.strftime('%Y-%m-%dT%H:%M:%SZ')

    params = {'q': news_keywords, 'from': start, 'to': end, 'language': 'en', 'sortBy': 'popularity', 'apiKey': api_key}

    response = requests.get(URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get('articles', [])
