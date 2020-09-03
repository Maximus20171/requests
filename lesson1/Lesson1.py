# Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле json

import requests
import json
main_link = 'https://api.github.com/users/'
name='Maximus20171' #Имя пользователя
response=requests.get(main_link+name+'/repos')
j_data=response.json()

new_j={}
print(f"Список репозиториев клиента {name}:")
for i in range(len(j_data)):
    repository=j_data[i]['full_name'].replace(name+'/','')
    print(str(i+1)+') '+repository)
    new_j[i+1]=repository

with open('lesson1.json', "w", encoding="utf-8") as file:
    json.dump(new_j, file)