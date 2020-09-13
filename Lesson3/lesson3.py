# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД

# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы.
# Поиск по двум полям (мин и макс зарплату)
# 3) Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient

main_link = 'https://hh.ru'
main_link1 = 'superjob.ru'
area = {
    'россия': [113, 'russia.'],
    'москва': [1, ''],
    'санкт-петербург': [2, 'spb.'],
    'уфа': [99, 'ufa.'],
    'республика башкортостан': [1347, 'bashkortostan.']
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)
db = client['job_db']

while True:
     city= input('Где будем искать: ').lower()
     if city in area.keys():
         break
     else:
         print('нет таког города')
         print()
         print(f'Введите один из списка {area.keys()}')
vacancy=input('Вакансия: ')


## параметры для hh.ru
params = {'clusters': 'true',
          'enable_snippets': 'true',
          'text': vacancy,
          'L_save_area': 'true',
          'area': {area[city][0]},
          'from': 'cluster_area',
          'showClusters': 'true'
          }

## параметры для superjob.ru
params1 = {'keywords': vacancy,
           'page': 1
           }


## функция для определения минимума/максимуму и валюты ЗП
def salary(salary_str):
    min_max_c = [None, None, None]
    if salary_str == 'По договорённости':
        return min_max_c
    if salary_str:
        tmp = salary_str.replace('\xa0', ' ')
        k = 0
        tmp1 = list(tmp)
        diap = [x for x in range(48, 56)]
        for s in tmp[1:-2]:
            k += 1
            if (s == ' ') and (ord(tmp[k - 1]) in diap) and (ord(tmp[k + 1]) in diap):
                tmp1[k] = '!'
                tmp = ''.join(tmp1)
                # print(tmp)
        tmp = tmp.replace('!', '')
        # print('=',tmp)
        if salary_str[0] == 'о':
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = None
            min_max_c[0] = float(tmp.split()[1])
        elif salary_str[0] == 'д':
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = float(tmp.split()[1])
            min_max_c[0] = None
        elif salary_str.find('-') > -1:
            tmp = tmp.split('-')
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = float(tmp[1].split()[0])
            min_max_c[0] = float(tmp[0])
        else:
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = float(tmp.split()[0])
            min_max_c[0] = float(tmp.split()[0])
    return min_max_c


def salary_higher_than(salary_nuber):
    result = db.job.find({'$or': [{"salary_min": {'$gt': salary_nuber}}, {"salary_max": {'$gt': salary_nuber}}]}, {'_id': 0})
    print('\nСписок вакансий:')
    index = 0
    for i in result:
        pprint(i)
        index += 1
    print(f'Всего найденно вакансий: {index}')

def db_updata(DF_list):
    db.job.delete_many({}) # Удаляем БД
    db.job.insert_many(DF_list) #Вводим свежие данные

html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
soup = bs(html.text, 'html.parser')
vacancies_block = soup.find('div', {'class': 'sticky-container'})
vacancies_list2 = vacancies_block.find_all('div', {'class': 'vacancy-serp-item__row'})

html1 = requests.get('https://' + area[city][1] + main_link1 + '/vacancy/search/', params=params1, headers=headers)
soup1 = bs(html1.text, 'html.parser')
vacancies_block_sj = soup1.find('div', {'class': '_1Ttd8 _2CsQi'})
vacancies_list2_sj = vacancies_block_sj.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})

DataFrame_list=[] # Список словарей для добавления в БД

# Парсер для superjob
ii = 0
while True:
    soup1 = bs(html1.text, 'html.parser')
    vacancies_block_sj = soup1.find('div', {'class': '_1Ttd8 _2CsQi'})
    vacancies_list2_sj = vacancies_block_sj.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})
    #DataFrame_job = {}

    for i in vacancies_list2_sj:
        vacancies_list3_st = i.find('a', {'target': '_blank'})
        DataFrame_job = {}
        if vacancies_list3_st:
            ii += 1
            #print(f'{ii}ая вакансия')
            DataFrame_job['id']=ii ##добавляем Id
            #pprint(vacancies_list3_st.get_text())
            DataFrame_job['name']=vacancies_list3_st.get_text() ##добавляем название вакансии
            #pprint('https://' + area[city][1] + main_link1 + vacancies_list3_st.get('href'))
            DataFrame_job['href']=str('https://' + area[city][1] + main_link1 + vacancies_list3_st.get('href')) ## ссылка
            DataFrame_job['site']='superjob.ru' #сайт

            vacancies_list4_st = i.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
            if vacancies_list4_st:
                mas = salary(vacancies_list4_st.get_text())
            else:
                mas = [None, None, None]

            DataFrame_job['salary_min']=mas[0]
            DataFrame_job['salary_max']=mas[1]
            DataFrame_job['salary_currency']=mas[2]

            DataFrame_list.append(DataFrame_job)
            #db.users.insert_one(DataFrame_job['id'][ii-1])
            #print(mas)

    vv_st = vacancies_block_sj.find('a', {'rel': 'next'})
    try:
        vv_st.get('href')
    except AttributeError:
        break
    else:
        html1 = requests.get('https://' + area[city][1] + main_link1 + vv_st.get('href'), headers=headers)

# Парсер для НН
while True:
    soup = bs(html.text, 'html.parser')
    vacancies_block = soup.find('div', {'class': 'sticky-container'})
    vacancies_list2 = vacancies_block.find_all('div', {'class': 'vacancy-serp-item__row'})

    for i in vacancies_list2:
        vacancies_list3 = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        DataFrame_job = {}
        if vacancies_list3:
            ii += 1
            #print(f'{ii}ая вакансия')
            DataFrame_job['id']=ii
            #pprint(vacancies_list3.get_text())
            DataFrame_job['name']=vacancies_list3.get_text()
            #pprint(vacancies_list3.get('href'))
            DataFrame_job['href']=vacancies_list3.get('href')
            DataFrame_job['site']='hh.ru'

            vacancies_list4 = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vacancies_list4:
                mas = salary(vacancies_list4.get_text())
            else:
                mas = [None, None, None]
            DataFrame_job['salary_min']=mas[0]
            DataFrame_job['salary_max']=mas[1]
            DataFrame_job['salary_currency']=mas[2]
            DataFrame_list.append(DataFrame_job)
            #db.users.insert_one(DataFrame_job({'id':ii}))
            #print(mas)

    vv = vacancies_block.find('a', {'data-qa': 'pager-next'})
    print(vv)
    try:
        vv.get('href')
    except AttributeError:
        break
    else:
        html = requests.get(main_link + vv.get('href'), params=params, headers=headers)
        #print(main_link + vv.get('href'))
        #print(html)

print()
pprint(DataFrame_list)
#db.job.insert_many(DataFrame_list) # добавили 1 раз! и убрали строку в архив

# обновляем БД
db_updata(DataFrame_list)

# ищим ЗП больше чем заданныая
salary_search = None
while not salary_search:
    try:
        salary_search = int(input('Введите минимальную желаемую зарплату: '))
    except:
        print('Это не число')
        salary_search = None

salary_higher_than(salary_search)
