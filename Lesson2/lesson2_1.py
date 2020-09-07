# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:

# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'https://hh.ru'
area = {
    'Россия': 113,
    'Москва': 1,
    'Санкт-Петербург': 2,
    'Уфа': 99,
    'Республика Башкортостан': 1347
        }
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
# city= input('Введиие город: ')
city='Уфа'
params = {'clusters':'true',
          'enable_snippets':'true',
          'text': 'Python',
          'L_save_area':'true',
          'area': {area[city]},
          'from': 'cluster_area',
          'showClusters': 'true'
          }

html = requests.get(main_link + '/search/vacancy',params=params,headers=headers)
print(html)
#print('https://www.'+area[city][1]+main_link + '/search/vacancy',params=params,headers=headers)
soup = bs(html.text, 'html.parser')
vacancies_block = soup.find('div',{'class':'vacancy-serp'})
#vacancies_list1 = vacancies_block.find_all('span',{'data-qa': 'vacancy-serp__vacancy-compensation'})
vacancies_list2 = vacancies_block.find_all('a',{'class': 'bloko-link HH-LinkModifier'})

# pprint(len(vacancies_list1))
pprint(len(vacancies_list2))

ss=0
for i in vacancies_list2:
    vacan_data={}
    vacan_data['name']=i.get_text()
    vacan_data['href']=i.get('href')
    vacan_data['cite']=main_link
    vacancies_list1=vacancies_list2.parents['spam']
    pprint(vacancies_list1)
    salary=vacancies_list1[ss].get_text()
    print(salary.replace(' ', ''))

    vacan_data['salary_min']=None
    vacan_data['salary_max'] = None
    vacan_data['salary_currency'] = None
    #vacan_data.append(vacan_data)
    ss+=1

pprint(vacan_data)
