from newscover.newsapi import fetch_latest_news 
import json
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='News articles collection tool')
    parser.add_argument('-k', '--api_key', required=True, help='API key required to fetch news')
    parser.add_argument('-b', '--lookback', type=int, default=10, help='Range of days from today, 10 days if not specified')
    parser.add_argument('-i', '--input_file', required=True, help='Input JSON file with keyword lists')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory to save results')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, args.input_file)

    with open(json_path) as f:
        keywords = json.load(f)
    
    for n, k in keywords.items():
        words = ' OR '.join(k)
        articles = fetch_latest_news(args.api_key, words, lookback_days=args.lookback)

        name = n + '.json'
        output_file = os.path.join(args.output_dir, name)
        with open(output_file, 'w') as fi:
            json.dump(articles, fi, indent=2)

if __name__ == '__main__':
    main()