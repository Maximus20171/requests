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

# city= input('Где будем искать: ')
city='Россия'

main_link = 'https://hh.ru'
main_link1 = 'superjob.ru'
area = {
    'Россия': [113, 'russia.'],
    'Москва': [1, ''],
    'Санкт-Петербург': [2, 'spb.'],
    'Уфа': [99, 'ufa.'],
    'Республика Башкортостан': [1347,'bashkortostan.']
        }
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

## параметры для HH
params = {'clusters':'true',
          'enable_snippets':'true',
          'text': 'Python',
          'L_save_area':'true',
          'area': {area[city][0]},
          'from': 'cluster_area',
          'showClusters': 'true'
          }

## параметры для superjob
params1 = {'keywords':'python',
           'page':1
           }

## функция для определения минимума/максимуму и валюты ЗП
def salary (cite, salary_str):
    min_max_c=[None,None,None]
    if cite.find('hh') > -1 and salary_str:
        tmp = salary_str.replace('\xa0', ' ')
        k=0
        for s in tmp[1:-2]:
            k+=1
            if (s==' ') and (ord(tmp[k-1]) == 48) and (ord(tmp[k+1]) == 48):
                tmp[k]='!'
                print(s.index())
        #tmp = tmp.replace(' ', '')
        #if tmp[-1]=='.':
        #   tmp=tmp[0:-1]
        print(ord('9'))
        print('=',tmp)
        if salary_str[0]=='о':
            min_max_c[2]=salary_str.split()[-1]
            min_max_c[1] = None
            min_max_c[0] = float(tmp.split()[1])
        elif salary_str[0]=='д':
            min_max_c[2]=salary_str.split()[-1]
            min_max_c[1] = float(tmp.split()[1])
            min_max_c[0] = None
        elif salary_str.find('-')>-1:
            tmp = tmp.split('-')
            print(tmp)
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] =tmp[1].split()[0]
            min_max_c[0] =tmp[0]
        else:
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] =tmp.split()[0]
            min_max_c[0] =tmp.split()[0]

    elif cite.find('superjob') > -1 and salary_str:
        tmp = salary_str.replace('\xa0', ' ')
        print(tmp)
    return min_max_c




html = requests.get(main_link + '/search/vacancy',params=params,headers=headers)
soup = bs(html.text, 'html.parser')
vacancies_block = soup.find('div',{'class':'sticky-container'})
vacancies_list2 = vacancies_block.find_all('div',{'class': 'vacancy-serp-item__row'})
#print(len(vacancies_block))

html1 = requests.get('https://'+area[city][1]+main_link1+'/vacancy/search/' ,params=params1,headers=headers)
soup1 = bs(html1.text, 'html.parser')
#vacancies_block_sj = soup.find('div',{'class':'sticky-container'})
#https://bashkortostan.superjob.ru/vacancy/search/?keywords=python
#print(html1)
vacancies_block_sj = soup1.find('div',{'class':'_1Ttd8 _2CsQi'})
#pprint(vacancies_block_sj)
vacancies_list2_sj = vacancies_block_sj.find_all('div',{'class': 'jNMYr GPKTZ _1tH7S'})
pprint(len(vacancies_list2_sj))


st = 'от\xa030\xa0000\xa0руб.'

k=salary('hh',st )
print(k)

# 98ая вакансия
# 'Senior ML Engineer'
# 'до 130\xa0000 руб.'
# 'от 3\xa0000 USD'
# '80\xa0000-140\xa0000 руб.'
# 'Python Developer'
# 'https://ufa.hh.ru/vacancy/38650571?query=Python'
# '120\xa0000-150\xa0000 руб.'


# 'от\xa0150\xa0000\xa0руб.'
# 'По договорённости'
# 'от\xa025\xa0000\xa0руб.'
# 'от\xa030\xa0000\xa0руб.'
# '120\xa0000\xa0—\xa0150\xa0000\xa0руб.'
# '110\xa0000\xa0руб.'


#<a class="icMQ_ _6AfZ9 f-test-link-Razrabotchik_Ruby _2JivQ _1UJAN" target="_blank" href="/vakansii/razrabotchik-ruby-34363353.html?search_id=aeb897a6-f145-11ea-80e5-8d26d236fda7&amp;vacancyShouldHighlight=true">Разработчик Ruby</a>
#<span class="_3mfro _2Wp8I PlM3e _2JVkc _2VHxz">По договорённости</span>

ii=0

# while True:
#     soup1 = bs(html1.text, 'html.parser')
#     vacancies_block_sj = soup1.find('div', {'class': '_1Ttd8 _2CsQi'})
#     vacancies_list2_sj = vacancies_block_sj.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})
#
#     for i in vacancies_list2_sj:
#         vacancies_list3_st = i.find('a', {'target': '_blank'})
#         if vacancies_list3_st:
#             ii += 1
#             print(f'{ii}ая вакансия')
#             pprint(vacancies_list3_st.get_text())
#             pprint('https://'+area[city][1]+main_link1+vacancies_list3_st.get('href'))
#         vacancies_list4_st = i.find('span',{'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
#         if vacancies_list4_st:
#             pprint(vacancies_list4_st.get_text())
#
#     vv_st = vacancies_block_sj.find('a', {'rel': 'next'})
#     try:
#         vv_st.get('href')
#     except AttributeError:
#         break
#     else:
#         html1= requests.get('https://'+area[city][1]+main_link1 + vv_st.get('href'), headers=headers)


# ii=0 ##
# while True:
#     soup = bs(html.text, 'html.parser')
#     vacancies_block = soup.find('div', {'class': 'sticky-container'})
#     vacancies_list2 = vacancies_block.find_all('div', {'class': 'vacancy-serp-item__row'})
#
#     for i in vacancies_list2:
#         vacancies_list3 = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
#         if vacancies_list3:
#             ii += 1
#             print(f'{ii}ая вакансия')
#             pprint(vacancies_list3.get_text())
#         vacancies_list4 = i.find('span',{'data-qa': 'vacancy-serp__vacancy-compensation'})
#         if vacancies_list4:
#             pprint(vacancies_list4.get_text())
#
#     vv= vacancies_block.find('a',{'data-qa':'pager-next'})
#     print(vv)
#     try:
#         vv.get('href')
#     except AttributeError:
#         break
#     else:
#         html= requests.get(main_link+vv.get('href'), params=params,headers=headers)
#         print(main_link+vv.get('href'))
#         print(html)


    #pprint(vacancies_list3)
    #pprint(vacancies_list4.text)
#     try:
#         pprint(vacancies_list3.text)
#     except AttributeError:
#         pprint(None)
#
#     try:
#         pprint(vacancies_list4.text)
#     except AttributeError:
#         pprint(None)


# for i in vacancies_list2:
#     vacancies_list3 = i.find('a',{'data-qa': 'vacancy-serp__vacancy-title'})
#     vacancies_list4 = i.find('span',{'data-qa': 'vacancy-serp__vacancy-compensation'})
#     pprint(vacancies_list3.text)
#     pprint(vacancies_list4.text)

# pprint(vacancies_list2.text)
# pprint(vacancies_list3.text)
# pprint(vacancies_list4.text)
#print(vacancies_list2.next)
# <div class="vacancy-serp-item__row vacancy-serp-item__row_header"><div class="vacancy-serp-item__info"><span class="bloko-section-header-3 bloko-section-header-3_lite"><span class="resume-search-item__name"><span class="g-user-content"><a class="bloko-link HH-LinkModifier" data-qa="vacancy-serp__vacancy-title" href="https://ufa.hh.ru/analytics_source/vacancy/38976715?query=Python&amp;position=0&amp;requestId=1599497493834c72a56b2ed51730da08&amp;totalVacancies=56&amp;source=vacancies" data-position="0" data-requestid="1599497493834c72a56b2ed51730da08" data-totalvacancies="56" target="_blank" data-clicked="true">Python-разработчик</a></span></span></span></div><div class="vacancy-serp-item__sidebar"><span class="bloko-section-header-3 bloko-section-header-3_lite" data-qa="vacancy-serp__vacancy-compensation">30&nbsp;000-70&nbsp;000 руб.</span></div></div>
# pprint(len(vacancies_list1))

# for i in vacancies_block:
#     pprint(i)
#     break


# vacancies_list1 = vacancies_block.find_all('span',{'data-qa': 'vacancy-serp__vacancy-compensation'})
# vacancies_list2 = vacancies_block.find_all('a',{'class': 'bloko-link HH-LinkModifier'})
# pprint(vacancies_list1)
# pprint(vacancies_list2)

# vacancies_list1 = vacancies_block.find_next('span')
# vacancies_list2 = vacancies_block.find_next('a')
# pprint(vacancies_list1)
# pprint(vacancies_list2)
# ss=0
# for i in vacancies_list2:
#     vacan_data={}
#     vacan_data['name']=i.get_text()
#     vacan_data['href']=i.get('href')
#     vacan_data['cite']=main_link
#
#     salary=vacancies_list1[ss].get_text()
#     print(salary.replace(' ', ''))
#
#     vacan_data['salary_min']=None
#     vacan_data['salary_max'] = None
#     vacan_data['salary_currency'] = None
#     #vacan_data.append(vacan_data)
#     ss+=1

#pprint(vacan_data)
