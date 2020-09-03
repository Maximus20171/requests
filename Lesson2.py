#2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# https://oauth.vk.com/authorize?client_id=11032734
# &display=page&redirect_uri=http://example.com/callback&scope=friends&response_type=token&v=5.122&state=123456

# https://oauth.vk.com/blank.html#
# access_token=e4823c56aea170086a1f87d9a5098a187f0f13d345b3daaa6b1818262330fd8f2626b26460c68e02840cc&expires_in=86400&user_id=11032734

import requests
main_link = 'https://api.vk.com/method/users.get?user_id=11032734&v=5.52'
access_token='e4823c56aea170086a1f87d9a5098a187f0f13d345b3daaa6b1818262330fd8f2626b26460c68e02840cc'
response=requests.get(main_link+access_token)
print(response)

## Список моих друзей которые сейчас находятся на сайте
frends= "https://api.vk.com/method/friends.getOnline?v=5.52&access_token="
response1=requests.get(frends+access_token)
print(response1.text)

file = open('lesson2.txt', 'w', encoding="utf-8")
file.write('Ответ сервера: '+str(response.status_code)+'\n'+response1.text)
file.close()