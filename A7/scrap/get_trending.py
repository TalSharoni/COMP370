import requests
from bs4 import BeautifulSoup

output = 'scrap/out/output.html'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def fetch_trending():
    with open(output, 'r', encoding='utf-8') as file:
        html = file.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    trending_section = soup.find('div', {'data-tb-region': 'Top trending'})
    articles = trending_section.find_all('li', {'data-carousel-item': True})

    for idx, article in enumerate(articles, start=1):
        link = article.find('a', href=True)

        url = link['href']
        url = 'https://montrealgazette.com/' + url
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            article_html = response.text

            output_file = f"trendings/data/trending{idx}.html"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(article_html)

        else:
            raise Exception(response.status_code)


if __name__ == "__main__":
    fetch_trending()