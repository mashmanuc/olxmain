# -*- codecs: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import csv

URL = 'https://nz.ua/'

# ______________________________________________________________________________________________
# xpat шляхи для класів
m5 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[3]/td[2]/a[1]'
m6 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[3]/td[2]/a[2]'
a7 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[1]/td[2]/a[1]'
a8 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[1]/td[2]/a[2]'
a9 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[1]/td[2]/a[3]'
h7 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[2]/td[2]/a[1]'
h8 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[2]/td[2]/a[2]'
h9 = '//*[@id="page"]/div[2]/div[1]/div/div/table[1]/tbody/tr[2]/td[2]/a[3]'
# _________________________________________________________________________________________


# def klas():
#     """Функція вибирає хурнал класу"""
#     kl = input(f'Введіть клас---')
#     if kl == 'm5':
#         ks = m5
#     elif kl == 'm6':
#         ks = m6
#     elif kl == 'a7':
#         ks = a7
#     elif kl == 'a8':
#         ks = a8
#     elif kl == 'a9':
#         ks = a9
#     elif kl == 'h7':
#         ks = h7
#     elif kl == 'h8':
#         ks = h8
#     elif kl == 'h9':
#         ks = h9
#     else:
#         print(f'Повторіть щераз')
#         klas()
#     return ks

# ______________________________________________________________________________________________________________
# Робота з файлами
# ______________________________________________________________________________________________________________
file_params = 'params.csv'
m5csv = 'm5.csv'
m6csv = 'm6.csv'
kal_5 = 'm5.txt'
kal_6 = 'm6.txt'

# ____________________________________________________________________________________________________________


def openfile_csv(file_params):
    """Функція зчитує логін і пароль користувача
    """
    with open(file_params, 'r', encoding='utf-8') as f:
        auth = []
        for line in f:
            auth.append(line)

    return auth
# ____________________________________________________________________________________________________________


def biblioteka(kal_txt):
    """Переводить текстове календарне планування в json формат 
    """
    with open(kal_txt, 'r', encoding='utf-8') as file:
        kal = []
        for line in file:
            kal.append(line)
    forma = []
    radki = (len(kal))

    for line in kal:
        r = {
            'numer': (line[0: 5]).strip(),
            'data': (line[5: 11]).strip(),
            'tema': (line[11:]).strip()
        }
        forma.append(r)
    return forma


def save_doc(items, path):
    """Записує в csv файл 'path' документ 'items'"""
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['numer', 'data', 'tema'])
        for item in items:
            writer.writerow([item['numer'], item['data'],
                            item['tema']])

# ___________________________________________________________________________________________________________________
# ___________________________________________________________________________________________________________________


def init_driver():
    # Запескаєм браузер
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 1)
    return driver

# _______________________________________________________________________________________________________________


def lookup(driver, login, password):
    driver.get(URL)
    # Відкриваємо журнал
    try:
        box1 = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "LoginForm[login]")))
        box2 = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "LoginForm[password]")))
        button_vchod = driver.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#login-form > fieldset > div:nth-child(5) > a.ms-button.form-submit-btn')))
        box1.send_keys(login)
        box2.send_keys(password)
        button_vchod.click()
        driver.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#page > div.main.clear > ul > li.magazines-menu> a'))).click()

    except TimeoutException:
        print("Box or Button not found in google.com")


# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
login = openfile_csv(file_params)[0]
password = openfile_csv(file_params)[1]

if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, login, password)
# _______________________________________________________________________________________________________________
# kl = klas()
# Заходимо в  клас
kl = m6
driver.find_element_by_xpath(kl).click()
# ________________________________________________________________________________________________________________
# main_page = driver.page_source
# current_page_number = int(driver.find_element_by_css_selector(
#     '#page > div.main.clear > div.content > div > ul.pagination > li.active > a').text)
# print(current_page_number)
# __________________________________________________________________________________________________________________


def storinku():
    """ Функція , яка рахує кількість сторінок поточного журналу"""
    current_page_number = int(driver.find_element_by_css_selector(
        '#page > div.main.clear > div.content > div > ul.pagination > li.active > a').text)
    while True:
        # print(f"Processing page {current_page_number}..")

        try:
            next_page_link = driver.find_element_by_xpath(
                f'//*[@id="page"]/div[2]/div[1]/div/ul[2]/li[{current_page_number+1}]/a')
            next_page_link.click()
            # print(current_page_number)
            current_page_number += 1
        except (NoSuchElementException):
            # print(f"Exiting. Last page: {current_page_number}.")
            break
    return current_page_number-1


n = storinku()
print('storinku=', n)
# ____________________________________________________________________________


def urok():
    """Шукфє і виводить перший незаписаний урок на сторінці журналу"""
    nomer_v_spisku = 1
    while True:
        try:
            if int(driver.find_element_by_xpath(
                f'//*[@id="page"]/div[2]/div[1]/div/ul[3]/li[{nomer_v_spisku+1}]/div[1]/div[2]').text)-int(driver.find_element_by_xpath(
                    f'//*[@id="page"]/div[2]/div[1]/div/ul[3]/li[{nomer_v_spisku}]/div[1]/div[2]').text) == 1:
                nomer_v_spisku += 1
            else:
                print('n =', nomer_v_spisku)
        except:

            break

    return nomer_v_spisku+1
    # //*[@id = "page"]/div[2]/div[1]/div/ul[3]/li[     2      ]/div[1]/div[2]
# ___________________________________________________________________________


"""Входимо в редактор запису журналу"""
i = urok()
driver.find_element_by_xpath(
    f'//*[@id = "page"]/div[2]/div[1]/div/ul[3]/li[{i}]/div[1]/a').click()

# __________________________________________________________________________
