#!/usr/bin/python
"""Перевіряємо що витягує суп
"""
import requests
from bs4 import BeautifulSoup
import csv
import codecs
import time
infa = 'inform.csv'
HOST = 'https://www.olx.ua'
URL = 'https://coderoad.ru/34324498/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


def get_html(url, params=''):
    # функція яка забирає          з сторінки по вказаному URL-адресу і параметру --- html
    r = requests.get(url, headers=HEADERS, params=params)
    return r.content


html = get_html('https://www.olx.ua/transport/')
soup = BeautifulSoup(html, 'html.parser')
items = soup.find_all('tr', class_='wrap')
f = items[0].find('small').get_text('span').strip(),
print(soup)
