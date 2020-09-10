# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:

# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd

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

while True:
    city= input('Где будем искать: ').lower()
    if city in area.keys():
        break
    else:
        print('нет таког города')
        print()
        print(f'Введите один из списка {area.keys()}')

vacancy=input('Вакансия: ')

## параметры для HH
params = {'clusters': 'true',
          'enable_snippets': 'true',
          'text': vacancy,
          'L_save_area': 'true',
          'area': {area[city][0]},
          'from': 'cluster_area',
          'showClusters': 'true'
          }

## параметры для superjob
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
            min_max_c[1] = tmp[1].split()[0]
            min_max_c[0] = tmp[0]
        else:
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = tmp.split()[0]
            min_max_c[0] = tmp.split()[0]

    return min_max_c


html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
soup = bs(html.text, 'html.parser')
vacancies_block = soup.find('div', {'class': 'sticky-container'})
vacancies_list2 = vacancies_block.find_all('div', {'class': 'vacancy-serp-item__row'})

html1 = requests.get('https://' + area[city][1] + main_link1 + '/vacancy/search/', params=params1, headers=headers)
soup1 = bs(html1.text, 'html.parser')
vacancies_block_sj = soup1.find('div', {'class': '_1Ttd8 _2CsQi'})
vacancies_list2_sj = vacancies_block_sj.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})

DataFrame_job= {'id':[],
                'name': [],
                'href': [],
                'salary_min': [],
                'salary_max': [],
                'salary_currency': [],
                'site': []
                }


# Парсер для superjob
ii = 0
while True:
    soup1 = bs(html1.text, 'html.parser')
    vacancies_block_sj = soup1.find('div', {'class': '_1Ttd8 _2CsQi'})
    vacancies_list2_sj = vacancies_block_sj.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})

    for i in vacancies_list2_sj:
        vacancies_list3_st = i.find('a', {'target': '_blank'})
        if vacancies_list3_st:
            ii += 1
            print(f'{ii}ая вакансия')
            DataFrame_job['id'].append(ii) ##добавляем Id
            pprint(vacancies_list3_st.get_text())
            DataFrame_job['name'].append(vacancies_list3_st.get_text()) ##добавляем название вакансии
            pprint('https://' + area[city][1] + main_link1 + vacancies_list3_st.get('href'))
            DataFrame_job['href'].append('https://' + area[city][1] + main_link1 + vacancies_list3_st.get('href')) ## ссылка
            DataFrame_job['site'].append('superjob.ru') #сайт

            vacancies_list4_st = i.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
            if vacancies_list4_st:
                mas = salary(vacancies_list4_st.get_text())
            else:
                mas = [None, None, None]
            DataFrame_job['salary_min'].append(mas[0])
            DataFrame_job['salary_max'].append(mas[1])
            DataFrame_job['salary_currency'].append(mas[2])
            print(mas)

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
        if vacancies_list3:
            ii += 1
            print(f'{ii}ая вакансия')
            DataFrame_job['id'].append(ii)
            pprint(vacancies_list3.get_text())
            DataFrame_job['name'].append(vacancies_list3.get_text())
            pprint(vacancies_list3.get('href'))
            DataFrame_job['href'].append(vacancies_list3.get('href'))
            DataFrame_job['site'].append('hh.ru')

            vacancies_list4 = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vacancies_list4:
                mas = salary(vacancies_list4.get_text())
            else:
                mas = [None, None, None]
            DataFrame_job['salary_min'].append(mas[0])
            DataFrame_job['salary_max'].append(mas[1])
            DataFrame_job['salary_currency'].append(mas[2])
            print(mas)

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
#pprint(DataFrame_job)

# Сохраняем файл в вакансий
pd.DataFrame(DataFrame_job).to_csv('vacancies.csv', index=False, encoding='windows-1251')
print('Вакансии сохранены в файде vacancies.csv')
