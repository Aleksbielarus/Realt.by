from bs4 import BeautifulSoup
import requests
import csv
import Connection
import time

URL = 'https://realt.by/sale/flats/'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
accept = '*/*'
HEADERS = {'user-agent': user_agent, 'accept': accept}
FILE = 'flats.csv'
dbname = 'postgres'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('div', class_='paging-list')
    pagination = int(pagination[-1].get_text()[-5:])  # need to fix
    return pagination


def select_max_date():
    db = Connection.connect(dbname)
    cursor = db.cursor()
    cursor.execute("SELECT to_char(max(parsing_date), 'YYYY.MM.DD') FROM data_source.tech_table")
    max_date = str(cursor.fetchall())[3:-4]
    db.close()
    return max_date


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item')
    flats = []
    pars_rows = 0
    error_rows = 0
    for item in items:
        try:
            try:
                time.strptime(item.find('div', class_='info-mini').find_all('span')[2].get_text(strip=True), "%d.%m.%Y")
                if time.strptime(item.find('div', class_='info-mini').find_all('span')[2].get_text(strip=True), "%d.%m.%Y") >= time.strptime(select_max_date(), "%d.%m.%Y"):
                    flats.append({
                        'id': item.find('span', class_='justify-content-md-end').get_text(strip=True),
                        'title': item.find('a', class_='teaser-title').get_text(strip=True),
                        'link': item.find('a', class_='teaser-title').get('href'),
                        'address': item.find('div', class_='location').get_text(strip=True),
                        # need to split for 3 col(room_num, square, floor)
                        'info': item.find('div', class_='info-large').get_text(strip=True),
                        'seller_name': item.find('span', class_='color-graydark').get_text(strip=True),
                        'seller_contact': item.find('span', class_='color-black').get_text(strip=True),
                        'img': item.find('img', class_='lazy').get('data-original'),
                        'usd_price': item.find('div', class_='col-auto').get_text(strip=True),
                        'byn_price': item.find('div', class_='fs-huge').get_text(strip=True),
                        'created_at': item.find('div', class_='info-mini').find_all('span')[2].get_text(strip=True)
                })
                    pars_rows += 1
            except ValueError:
                print('Date format error')
        except AttributeError:
            print('Attribute error in {} row')
            error_rows += 1
        # need to create log
        print(f'------row {pars_rows}')
        print(f'Total valid rows {pars_rows}')
        print(f'Total failed rows {error_rows}')
    return flats


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title',
                         'id',
                         'link',
                         'address',
                         'info',
                         'seller_name',
                         'seller_contact',
                         'img',
                         'usd_price',
                         'byn_price',
                         'created_at'
                         ])
        for item in items:
            writer.writerow([item['title'],
                             item['id'],
                             item['link'],
                             item['address'],
                             item['info'],
                             item['seller_name'],
                             item['seller_contact'],
                             item['img'],
                             item['usd_price'],
                             item['byn_price'],
                             item['created_at']
                             ])


def insert_last_update():
    if __name__ == "__main__":
        db = Connection.connect(dbname)
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute('''insert into data_source.tech_table(id, parsing_date, parsing_datetime)
                          values (DEFAULT,DEFAULT,DEFAULT);
                       ''')
        db.close()


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        flats = []
        page_count = get_page_count(html.text)
        for page in range(1, page_count+1):
            print(f'Parsing page {page} from {page_count}')
            html = get_html(URL, params={'page': page})
            flats.extend(get_content(html.text))
        save_file(flats, FILE)
        insert_last_update()
    else:
        print('Error')


parse()
