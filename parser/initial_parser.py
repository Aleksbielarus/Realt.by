from bs4 import BeautifulSoup
import requests
import csv

URL = 'https://realt.by/sale/flats/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36', 'accept': '*/*'}
#https://realt.by/sale/flats/?page=2

FILE = 'flats.csv'


def get_html (url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('div', class_= 'paging-list')
    pagination = int(pagination[-1].get_text()[-5:]) # need to fix
    return pagination


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item')
    flats = []
    pars_rows = 0
    error_rows = 0
    for item in items:
        try:
            flats.append({
                'title': item.find('a', class_='teaser-title').get_text(strip=True),
                'link': item.find('a', class_='teaser-title').get('href'),
                'address': item.find('div', class_='location').get_text(strip=True),
                'info': item.find('div', class_='info-large').get_text(strip=True), # need to split for 3 col(room_num, square, floor)
                'seller_name': item.find('span', class_='color-graydark').get_text(strip=True),
                'seller_contact': item.find('span', class_='color-black').get_text(strip=True),
                'img': item.find('img', class_='lazy').get('data-original'),
                'usd_price': item.find('div', class_='col-auto').get_text(strip=True),
                'byn_price': item.find('div', class_='fs-huge').get_text(strip=True)
            })
            pars_rows += 1
        except AttributeError:
            print('Attribute error in {} row')
            error_rows +=1

        # flats.append({
        #     'title': title,
        # })
        print(f'------row {pars_rows}')
        print(f'Total valid rows {pars_rows}')
        print(f'Total failed rows {error_rows}')
    return flats


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'link', 'address', 'info', 'seller_name', 'seller_contact', 'img', 'usd_price', 'byn_price'])
        for item in items:
            writer.writerow([item['title'],
                             item['link'],
                             item['address'],
                             item['info'],
                             item['seller_name'],
                             item['seller_contact'],
                             item['img'],
                             item['usd_price'],
                             item['byn_price']
                             ])

def parse():
    #
    html = get_html(URL)
    flats = []
    if html.status_code == 200:
        flats = []
        page_count = get_page_count(html.text)
        for page in range(1, page_count+1):
        #for page in range(1, 2):
            print(f'Parsing page {page} from {page_count}')
            html = get_html(URL, params={'page': page})
            flats.extend(get_content(html.text))
        save_file(flats, FILE)
    else:
        print('Error')

parse()

