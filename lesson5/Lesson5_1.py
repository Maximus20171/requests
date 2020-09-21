# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

from pymongo import MongoClient
from pprint import pprint
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://mail.ru/')

elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'mailbox:login-input')))
elem.send_keys('study.ai_172@mail.ru')
elem.submit()

elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'mailbox:password-input')))
elem.send_keys('NextPassword172')
elem.submit()

WebDriverWait(driver, 10).until(EC.title_contains('Входящие'))

client = MongoClient('127.0.0.1', 27017)
db = client['mail_ru']
mongo = db.incoming
# db.incoming.delete_many({}) # ИСПОЛЬЗОВАТЬ ПО МЕРЕ НЕОБХОДИМОСТИ

last_message = None
message_href=set()

while True:
    tmp = driver.find_elements_by_xpath('//a[contains(@class,"js-letter-list-item")]')
    message = tmp[-1]
    for i in range(len(tmp)):
        tmp[i] = tmp[i].get_attribute('href')

    if tmp[-1] == last_message:
        break

    for href in tmp:
        message_href.add(href)

    action = ActionChains(driver)
    action.move_to_element(message)
    action.perform()
    last_message = tmp[-1]


# pprint(message_href)
# print(len(tmp), len(message_href))
# print(tmp)

for item in message_href:
    driver.get(item)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))

    message_db = {}

    message_db['subject'] = element.text
    message_db['author_mail'] = driver.find_element_by_xpath(
        '//div[@class="letter__author"]/span').get_attribute('title')
    message_db['author_name'] = driver.find_element_by_xpath('//div[@class="letter__author"]/span').text

    date = driver.find_element_by_xpath('//div[@class="letter__date"]').text.split(',')
    time_form = time.strptime(time.ctime(time.time()), '%a %b %d %H:%M:%S %Y')

    if date[0] == 'Сегодня':
        message_db['date'] = time.strftime('%d %B', time_form) + ',' + date[1]
    elif date[0] == 'Вчера':
        day = str(int(time.strftime('%d', time_form)) - 1)
        message_db['date'] = day + time.strftime(' %B', time_form) + ',' + date[1]
    else:
        message_db['date'] = ','.join(date)

    message_db['text'] = driver.find_element_by_xpath('//div[contains(@id,"_BODY")]').text

    pprint(message_db)
    mongo.update_one({'author_name': message_db['author_name'], 'subject': message_db['subject']},{'$set':message_db}, upsert=True)
