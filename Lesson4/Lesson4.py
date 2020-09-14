# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

from pprint import pprint
from lxml import html
import requests
import datetime

lenta_link = 'https://lenta.ru/rubrics/economics/'
mail_link = 'https://news.mail.ru/economics/'
yandex_link='https://yandex.ru/news/rubric/business'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

lenta = requests.get(lenta_link, headers=headers)
mail=requests.get(mail_link, headers=headers)
yandex=requests.get(yandex_link, headers=headers)


all_news=[]

# lenta.ru. Экономика. Раздел "Последние новости"
dom_lenta=html.fromstring(lenta.text)
news=dom_lenta.xpath("//div[@class='b-yellow-box__wrap']/div[@class='item']")
for new in news:
    one_new={}
    one_new['source']= 'lenta.ru'
    one_new['name'] = new.xpath("./a/text()")[0]
    one_new['href'] = 'https://lenta.ru/'+new.xpath("./a/@href")[0]
    one_new['time']= new.xpath(".//time[@class='g-time']/@datetime")[0]
    all_news.append(one_new)

#pprint(all_news)


# new.yandex.ru. Экономика. Раздел "Последние новости"
dom_yandex=html.fromstring(yandex.text)
news=dom_yandex.xpath("//div[@class='news-card__inner']")
for new in news:
    one_new = {}
    one_new['source']=new.xpath(".//div[@class='mg-card-source news-card__source']//text()")[0]
    one_new['name']=new.xpath("./a//text()")[0]
    one_new['href']=new.xpath("./a/@href")[0]
    one_new['time']=new.xpath(".//div[@class='mg-card-source news-card__source']//text()")[1]
    all_news.append(one_new)

news=dom_yandex.xpath("//div[@class='mg-grid__col mg-grid__col_xs_4']/article")
for new in news:
    one_new = {}
    one_new['source']=new.xpath(".//span[@class='mg-card-source__source']//text()")[0]
    one_new['name']=new.xpath("./a//text()")[0]
    one_new['href']=new.xpath("./a/@href")[0]
    one_new['time']=new.xpath(".//span[@class='mg-card-source__time']//text()")[0]
    all_news.append(one_new)

#pprint(all_news)

# new.mail.ru. Экономика. Раздел "Последние новости"
dom_mail=html.fromstring(mail.text)
# Новости в картинках
news=dom_mail.xpath("//div[@class='grid margin_bottom_20']//a[@class='photo photo_small photo_scale photo_full grid__photo']")
for new in news:
    one_new = {}
    one_new['name']=new.xpath(".//span[@class='photo__title']//text()")[0]
    one_new['href']=new.xpath("./@href")[0]
    # Переходим на страницу новости
    html_mail1 = requests.get(one_new['href'], headers=headers)
    mail_page = html.fromstring(html_mail1.text)
    #Парсим ЕЕ
    one_new['time']=mail_page.xpath("//div[@class ='breadcrumbs breadcrumbs_article js-ago-wrapper']//span[@class ='note']//@datetime")[0]
    one_new['source']=mail_page.xpath("//div[@class ='breadcrumbs breadcrumbs_article js-ago-wrapper']//span[@class ='note']//text()")[2]
    all_news.append(one_new)

# новости ранее
news=dom_mail.xpath("//div[@class='paging__content js-pgng_cont']//div[@class='newsitem newsitem_height_fixed js-ago-wrapper js-pgng_item']")
for new in news:
    one_new = {}
    one_new['name']=new.xpath(".//a[@class='newsitem__title link-holder']//text()")[0]
    one_new['href']=new.xpath(".//a[@class='newsitem__title link-holder']/@href")[0]
    one_new['time']=new.xpath(".//div[@class='newsitem__params']/span[@class ='newsitem__param js-ago']/@datetime")[0]
    one_new['source']=new.xpath(".//div[@class='newsitem__params']//span[@class='newsitem__param']//text()")[0]
    all_news.append(one_new)


pprint(all_news)


