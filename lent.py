import requests  # работа c запроcами, вытягиваем инфу c cайта
from bs4 import BeautifulSoup  # делает cвой объект и работает c ним
import pandas as pd


URL1 = 'https://lenta.com/catalog/frukty-i-ovoshchi/'
URL2 = 'https://lenta.com/catalog/myaso-ptica-kolbasa/'
URL3 = 'https://lenta.com/catalog/bakaleya/'
URL4 = 'https://lenta.com/catalog/ryba-i-moreprodukty/'
URL5 = 'https://lenta.com/catalog/moloko-syr-yajjco/'
URL6 = 'https://lenta.com/catalog/chajj-kofe-kakao/'
URL7 = 'https://lenta.com/catalog/alkogolnye-napitki/'
URL8 = 'https://lenta.com/catalog/konditerskie-izdeliya/'
URL9 = 'https://lenta.com/catalog/zamorozhennaya-produkciya/'
URL10 = 'https://lenta.com/catalog/bezalkogolnye-napitki/'
URL11 = 'https://lenta.com/catalog/hleb-i-hlebobulochnye-izdeliya/'
URL = [URL1, URL2, URL3, URL4, URL5, URL6, URL7, URL8, URL9, URL10, URL11]

HOST = 'https://lenta.com'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'
}
COOKIES = {'.ASPXANONYMOUS': 'eqJYv_5OkBdmabkZugIbLlEbPiYLF5HqtXMMliG3yQt9csZ1nSKvNqyO-6eF0PLOPVMLLS1m1uXW'
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
                             '_ym_isad=2; _gid=GA1.2.1095021276.1667398892; '
                             'ValidationToken=e54c9793087a91a9994b18ae5e64915e; '
                             'ASP.NET_SessionId=x0o4o231p3gaw2yn2f5tmg3f; '
                             '_hjSessionUser_3225473=eyJpZCI6IjA0ZThlZjc3LWJkN2QtNTllNi04Mjg1LTNiYjUwZmYxM2Y2OSIsImNyZWF0ZWQiOjE2Njc0MDc1NzQ0MDcsImV4aXN0aW5nIjp0cnVlfQ==; ReviewedSkus=558630,168210,280267,515383,363352,103008,453565,260969,547550,123264,162743,370071; qrator_jsr=1667420599.686.14SddaHmNnX8NiLl-ttdl2f5d3g3m1hu8ff4oqgjlbt50qai8-00; qrator_jsid=1667420599.686.14SddaHmNnX8NiLl-jtlncpl0lu4hqasfaof6ou0e6mulm735; _ym_visorc=b; _gat_UA-327775-1=1; _dc_gtm_UA-327775-35=1; _dc_gtm_UA-327775-27=1; tmr_detect=0%7C1667420709087; tmr_reqNum=344'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params, cookies=COOKIES)
    return r

def get_content(html):
    products = []
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find_all('div', class_='sku-card-small-container')
    for item in title:
        name = item.find('div', class_='sku-card-small-header__title').get_text(strip=True)
        if item.find('div', class_="sku-card-small__labels").find('div', class_='discount-label-small '
                                                                                'discount-label-small--sku-card '
                                                                                'sku-card-small__discount-label') is not None:
            a = "Со cкидкой"
        else:
            a = 'Без cкидки'
        we = item.find('span', class_='sku-card-small-weight-options__item sku-card-small-weight-options__item--active')
        if we is None:
            we = "за 1 шт."
        else:
            we = "за 1 кг"
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
    df.to_csv("lenta.csv", mode='a')
    return products


for i in URL:
    for page in range(1,11):
        html = get_html(URL + f'?page={page}')
        print(URL + f'?page={page}')
        get_content(html.text)