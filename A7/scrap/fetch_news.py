import requests

URL = 'https://montrealgazette.com/category/news/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def fetch(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content

        with open('scrap/out/output.html', 'wb') as file:  
            file.write(html_content)

    else:
        raise Exception(response.status_code)
    
if __name__ == "__main__":
    fetch(URL)