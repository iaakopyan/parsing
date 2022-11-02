import re

import requests  # работа c запроcами, вытягиваем инфу c cайта
from bs4 import BeautifulSoup  # делает cвой объект и работает c ним
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
                              'IsAdult=True; '
                              'AddressTooltipInfo=Lenta.MainSite.Abstractions.Entities.Ecom.AddressTooltip; '
                              'ReviewedSkus=303639,364228,162743,574595,558630,168210,280267,515383,363352,103008,'
                              '453565,260969; ASP.NET_SessionId=q1m455bmfhlny3kclzhdobj1; _ym_isad=2; _ym_visorc=b; '
                              '_gid=GA1.2.1095021276.1667398892; ValidationToken=e54c9793087a91a9994b18ae5e64915e; '
                              '_dc_gtm_UA-327775-27=1; _dc_gtm_UA-327775-35=1; _gat_UA-327775-1=1; '
                              'qrator_jsid=1667398890.804.et9YKJbcFMCvoSVM-4t7ng1n5tvl56qqu08s8qdacqu2pff6c; '
                              'tmr_detect=0%7C1667400076933; tmr_reqNum=263'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params, cookies=COOKIES)
    return r


products = []


def get_content(html):
    global c
    c = ''
    for page in range(1, 11):
        print(f'page {page}')
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find_all('div', class_='sku-card-small-container')

        for item in title:
            name = item.find('div', class_='sku-card-small-header__title').get_text(strip=True)
            if item.find('div', class_="sku-card-small__labels").find('div', class_='discount-label-small '
                                                                                    'discount-label-small--sku-card '
                                                                                    'sku-card-small__discount-label') \
                    is not None:
                a = "cо cкидкой"
            else:
                a = 'Без cкидки'

            # if item.find('span',
            #             class_='sku-card-small-weight-options__item') is None:
            # if re.search('(?:\Sкг|\Sг|\Sл|\Sмл)', name) is not None:
            #     c = 'за 1 шт.'
            # elif item.find('span','sku-card-small-weight-options__item').get_text(strip=True) is not None:
            #     c = item.find('span','sku-card-small-weight-options__item').get_text(strip=True)
            #     #print(c)

            we = str(item.find('span',
                               class_='sku-card-small-weight-options__item sku-card-small-weight-options__item--active'))
            we = re.sub(
                '<span class="sku-card-small-weight-options__item sku-card-small-weight-options__item--active">', '',
                we)
            we = re.sub('</span>', '', we)
            we = re.sub('\r\n', '', we)
            we=we.strip()
            we = 'за ' + we
            we = re.sub('None', '1 шт.', we)
            products.append(
                {
                    'title': name,
                    'price': item.find('span', class_='price-label__integer').get_text(strip=True) + '.' + item.find(
                        'small', class_='price-label__fraction').get_text(strip=True) + ' руб.',
                    'weight': we,
                    'link_category': HOST + item.find('a').get('href'),
                    'sale': a
                }
            )
    print(products)
    df = pd.DataFrame(products)
    df.to_csv("lenta.csv")
    return products


for i in URL:
    html = get_html(i)
    get_content(html.text)
