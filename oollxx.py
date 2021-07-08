import requests
from bs4 import BeautifulSoup
import csv
import codecs
import time
FILENAME = 'olx_result.csv'
infa = 'inform.csv'
HOST = 'https://www.olx.ua'
URL = 'http://www.olx.ua/transport/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


def get_html(url, params=''):
    # функція яка забирає з сторінки по вказаному URL-адресу і параметру --- html
    r = requests.get(url, headers=HEADERS, params=params)
    return r.content


html = get_html('https://www.olx.ua/transport/')

# soup = BeautifulSoup(test, 'html.parser')
# items = soup.find_all('tr', class_='wrap')
# print(items)


def get_content(html):
    # витягує контент з HTML
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='wrap')
    time.sleep(1)
    cards = []

    for item in items:

        cards.append({
            'link_protuct': item.find('tr').find('a').get('href'),
            'name': item.find('h3', class_='lheight22 margintop5').find('a').find('strong').text,
            'misto': item.find('small').get_text('span').strip(),
            'id': item.find('table').get('data-id')})

    return cards


cards = get_content(html)
with open(FILENAME, mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(
        w_file, delimiter=";", lineterminator="\n")
    file_writer.writerow(['Посилання', 'Назва', 'Інформація', 'ID'])
    for item in cards:
        file_writer.writerow(
            [item['link_protuct'], item['name'], item['misto'], item['id']])

print(cards)
