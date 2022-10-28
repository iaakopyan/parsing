import re

import requests  # работа с запросами, вытягиваем инфу с сайта
from bs4 import BeautifulSoup  # делает свой объект и работает с ним
import pandas as pd

URL1 = 'https://lenta.com/catalog/frukty-i-ovoshchi/'
URL2 = 'https://lenta.com/catalog/myaso-ptica-kolbasa/'
URL3 = 'https://lenta.com/catalog/bakaleya/'
URL4 = 'https://lenta.com/catalog/ryba-i-moreprodukty/'
URL5 = 'https://lenta.com/catalog/moloko-syr-yayca/'
URL6 = 'https://lenta.com/catalog/chajj-kofe-kakao/'
URL7 = 'https://lenta.com/catalog/alkogolnye-napitki/'
URL8 = 'https://lenta.com/catalog/konditerskie-izdeliya/'
URL9 = 'https://lenta.com/catalog/zamorozhennaya-produkciya/'
URL10 = 'https://lenta.com/catalog/bezalkogolnye-napitki/'
URL12 = 'https://lenta.com/catalog/hleb-i-hlebobulochnye-izdeliya/'
URL = [URL1, URL2, URL3, URL4, URL5, URL6, URL7, URL8, URL9, URL10, URL12]

HOST = 'https://lenta.com'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'
}
COOKIES = {'..ASPXANONYMOUS': 'eqJYv_5OkBdmabkZugIbLlEbPiYLF5HqtXMMliG3yQt9csZ1nSKvNqyO-6eF0PLOPVMLLS1m1uXW'
                              '-Bal22nWqOkvHwPv86bUImcspQYW0NvdKThD9MTgQPGZsoup_7UG515vsw2; '
                              'cookiesession1=678B286D01234EFGHIJKLMNOPQRS2852; '
                              'CustomerId=9c943b0ba44f42e68859edbfb00d4f0b; ShouldSetDeliveryOptions=True; '
                              'DontShowCookieNotification=true; _tm_lt_sid=1666799776495.556779; '
                              '_ym_uid=1666799777452142477; _ym_d=1666799777; '
                              'KFP_DID=196bae9b-1e5f-8b52-95d5-d7b20055e4d4; _gcl_au=1.1.1537676024.1666799778; '
                              'tmr_lvid=441a6bef7f9fd77bc5e406d07386d837; tmr_lvidTS=1666799778430; '
                              '_ga=GA1.2.1208867502.1666799779; _a_d3t6sf=dulhIoKTf0Lh5jvbfvQFjjQC; '
                              '_tt_enable_cookie=1; _ttp=946a7cb9-a64b-4f9e-94a6-97b046716778; '
                              'flocktory-uuid=bcf94467-fbce-49ee-a211-0cd7902171e0-7; '
                              'oxxfgh=bfc274ae-57e6-4d34-a3be-be2bb140d666#0#5184000000#5000#1800000#44965; '
                              'ValidationToken=e8461631c36e40b26a7f7876ab8de3b7; _ym_isad=2; '
                              '_gid=GA1.2.639453384.1666907551; IsAdult=True; '
                              'ASP.NET_SessionId=kabdtq2zj5sblyxranopfi2m; ReviewedSkus=217386,300884,303639,364228,'
                              '162743,574595,558630,168210,280267; _ym_visorc=b; tmr_detect=0%7C1666945592818; '
                              'tmr_reqNum=143; '
                              'qrator_jsr=1666947337.191.BXWPHSuftmu43QDK-bp3etl9bue6rdllfbvl7pibkssp0ren3-00; '
                              'qrator_jsid=1666947337.191.BXWPHSuftmu43QDK-ltq3v14vf77tu7slhh1rrh9t8k6d5ghr'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params, cookies=COOKIES)
    return r


products = []


def get_content(html):
    for page in range(1, 2):
        print(f'page {page}')
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find_all('div', class_='sku-card-small-container')
        print(title)
        for item in title:
            name = item.find('div', class_='sku-card-small-header__title').get_text(strip=True)
            if item.find('div', class_="sku-card-small__labels").find('div', class_='discount-label-small '
                                                                                    'discount-label-small--sku-card '
                                                                                    'sku-card-small__discount-label') \
                    is not None:
                a = "Со скидкой"
            else:
                a = 'Без скидки'
            if item.find('span',
                         class_='sku-card-small-weight-options__item') is None:

                c = re.search('(?:[1-9]кг|[1-9][0-9]г|[1-9][0-9][0-9]г)', name)
                if c == None:
                    continue
                else:
                    name = re.sub('(?:, [1-9]кг|, [1-9][0-9]г|, [1-9][0-9][0-9]г)', '', name)
                    c = c.group()
                    c = re.sub('кг', ' кг', c)
                    c = re.sub('г', ' г', c)

            else:
                c = item.find('div',
                              class_='sku-card-small-weight-options__track').find('span',
                                                                                  'sku-card-small-weight-options__item sku-card-small-weight-options__item--active').get_text(
                    strip=True)

            products.append(
                {
                    'title': name,
                    'price': item.find('span', class_='price-label__integer').get_text(strip=True) + '.' + item.find(
                        'small', class_='price-label__fraction').get_text(strip=True) + ' руб.',
                    'weight': c,
                    'link_category': HOST + item.find('a').get('href'),
                    'sale': a
                }
            )
    print(products)
    df = pd.DataFrame(products)
    df.to_csv("lenta.csv")
    return products


# for i in URL:
html = get_html(URL1)
# print(html)
get_content(html.text)
