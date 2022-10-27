import requests  # работа с запросами, вытягиваем инфу с сайта
from bs4 import BeautifulSoup  # делает свой объект и работает с ним
import pandas as pd

URL1 = 'https://online.globus.ru/catalog/ovoshchi-frukty-zelen/'
URL2 = 'https://online.globus.ru/catalog/myaso-ptitsa-kolbasy/'
URL3 = 'https://online.globus.ru/catalog/bakaleya/'
URL4 = 'https://online.globus.ru/catalog/ryba-ikra-moreprodukty/'
URL5 = 'https://online.globus.ru/catalog/molochnye-produkty-syr-yaytsa/'
URL6 = 'https://online.globus.ru/catalog/chay-kofe-kakao/'
URL7 = 'https://online.globus.ru/catalog/alkogol/'
URL8 = 'https://online.globus.ru/catalog/chipsy-sneki-orekhi/'
URL9 = 'https://online.globus.ru/catalog/zamorozhennye-produkty/'
URL10 = 'https://online.globus.ru/catalog/bezalkogolnye-napitki/'
URL = [URL1, URL2, URL3, URL4, URL5, URL6, URL7, URL8, URL9, URL10]

HOST = 'https://online.globus.ru'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36 '
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_pages_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = []
    a = soup.find_all('a', class_='js-navigation__page ga-event')
    pagination.append(a)
    return len(pagination)-1


products = []


def get_content(html):
    for page in range(1, 20):
        print(f'page {page}')
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find_all('div', class_='catalog-section__item__body trans')
        print(title)
        for item in title:
            if item.find('span', class_="item-price__old") is not None:
                a = "Со скидкой"
            else:
                a = 'Без скидки'
            products.append(
                {
                    'title': item.find('span', class_='catalog-section__item__title').get_text(strip=True),
                    'price': item.find('span', class_='item-price__num').get_text(separator='.', strip=True),
                    'weight': item.find('span',
                                        class_='item-price__additional item-price__additional--solo').get_text(
                        strip=True),
                    'link_category': HOST + item.find('a').get('href'),
                    'sale': a
                }
            )
    print(products)
    df = pd.DataFrame(products)
    df.to_csv("globus.csv")
    return products


for i in URL:
    html = get_html(i)
    get_content(html.text)
