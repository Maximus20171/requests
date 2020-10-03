# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

## функция для определения минимума/максимуму и валюты ЗП
def salary_progress(salary_str, spider_name):
    min_max_c = [None, None, None]
    if salary_str[0] in ['По договорённости', 'з/п не указана']:
        return min_max_c
    else:
        if spider_name=='hhru':
            if salary_str[0].replace(' ','')=='от':
                p=0
                for st in salary_str[1:]:
                    sl= st.replace('\xa0', '')
                    if sl.lower() in ['руб.','usd','eur']:
                        min_max_c[2]=sl
                    try:
                        sl=float(sl)
                    except:
                        continue
                    else:
                        min_max_c[p]=sl
                        p=+1
            elif salary_str[0].replace(' ','')=='до':
                for st in salary_str[::-1]:
                    sl= st.replace('\xa0', '')
                    if sl.lower() in ['руб.','usd','eur']:
                        min_max_c[2]=sl
                    try:
                        sl=float(sl)
                    except:
                        continue
                    else:
                        min_max_c[1]=sl
                        break

        if spider_name=='sjru':
            if '—' in salary_str:
                min_max_c[0]= float(salary_str[0].replace('\xa0', ''))
                min_max_c[1] = float(salary_str[4].replace('\xa0', ''))
                min_max_c[2] = salary_str[-1].replace('\xa0', '')
            elif salary_str[0].replace(' ','')=='от':
                tmp = salary_str[2].replace('\xa0', ' ')
                position=tmp.rfind(' ')
                min_max_c[2]=tmp[position:]
                min_max_c[0]=float(tmp[:position].replace(' ',''))
            elif salary_str[0].replace(' ','')=='до':
                tmp = salary_str[2].replace('\xa0', ' ')
                position=tmp.rfind(' ')
                min_max_c[2]=tmp[position:]
                min_max_c[1]=float(tmp[:position].replace(' ',''))
            elif float(salary_str[0].replace('\xa0', ''))>0:
                min_max_c[0]=float(salary_str[0].replace('\xa0', ''))
                min_max_c[1] = float(salary_str[0].replace('\xa0', ''))
                min_max_c[2] = salary_str[2]
    return min_max_c


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        #client['vacancy'].delete_many({})
        self.mongobase = client.vacancy

    def process_item(self, item, spider):
        salarys =salary_progress(item['salary'], spider.name)
        #print(salarys)
        #vacansy = dict(item)
        # print(vacansy)

        collection = self.mongobase[spider.name]

        if spider.name=='hhru':
            collection.insert_one({'name': item['name'], 'min_salary':salarys[0],'max_salary':salarys[1],'currency':salarys[2],'href':item['href'],'site':'hh.ru'})

        if spider.name=='sjru':
             collection.insert_one({'name': item['name'], 'min_salary':salarys[0],'max_salary':salarys[1],'currency':salarys[2],'href':item['href'],'site':'superjob.ru'})

        #collection.update_one({'author_name': message_db['author_name'], 'subject': message_db['subject']}, {'$set': message_db}, upsert=True)
        return item

