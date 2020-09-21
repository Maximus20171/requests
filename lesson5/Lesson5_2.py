from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from pymongo import MongoClient
import time

browser_options = Options()
browser_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver', options=browser_options)

client = MongoClient('127.0.0.1', 27017)
db = client['db_mvideo']
mongo = db.hits
#db.hits.delete_many({})  # ИСПОЛЬЗОВАТЬ ПО МЕРЕ НЕОБХОДИМОСТИ

driver.get('https://www.mvideo.ru/')

h2 = driver.find_elements_by_xpath('//div[contains(@class,"h2")]')
index = None
for i in range(len(h2)):
    if 'Хиты' in h2[i].text:
        index = i
        break

if index == None:
    print('"Хиты продаж" не найдены!')
else:
    carousel_list = driver.find_elements_by_xpath('//ul[contains(@data-init,"galleryCarousel")]')
    print('"Хиты:"')

    while True:
        product_card_list = carousel_list[index].find_elements_by_xpath('./li/div')
        for i in range(4):
            product = {}
            product['name'] = product_card_list[i].find_element_by_xpath('.//h4').get_attribute('title')
            product['price'] = float(product_card_list[i].find_element_by_xpath('.//div[contains(@data-sel,"div-price_current")]').text.replace(' ', '')[:-1])
            pprint(product)
            mongo.update_one({'name': product['name'], 'price': product['price']},
                             {'$set': product}, upsert=True)

        button_next = carousel_list[index].find_element_by_xpath('./../../a[contains(@class,"next-btn")]')

        if 'disabled' in button_next.get_attribute('class'):
            break

        button_next.click()
        time.sleep(5)