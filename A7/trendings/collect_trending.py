from bs4 import BeautifulSoup
import json
import argparse

def collect_trending():
    parser = argparse.ArgumentParser(description="Retrieves details about the 5 trending news articles")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file")
    args = parser.parse_args()
    output = args.output

    articles = []

    for i in range(5):
        file = 'trendings/data/trending' + str(i+1) + '.html'
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find("h1", class_="article-title").text.strip() if soup.find("h1", class_="article-title") else ""
        date = soup.find("span", class_="published-date__since").text.strip() if soup.find("span", class_="published-date__since") else ""
        author = soup.find("span", class_="published-by__author").text.strip() if soup.find("span", class_="published-by__author") else ""
        blurb = soup.find("p", class_="article-subtitle").text.strip() if soup.find("p", class_="article-subtitle") else ""


        article_info = {
            "title": title,
            "publication_date": date,
            "author": author,
            "blurb": blurb
        }
        articles.append(article_info)

    with open(output, "w") as json_file:
        json.dump(articles, json_file, indent=2)

if __name__ == "__main__":
    collect_trending()