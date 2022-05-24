import requests
import time
from secrets import access_token, user_id

'''
проходится по группам в которых состоит пользователь, 
собирает всех членов этих групп,
выводит информацию о ФИО, онлайн-статусе, месте проживания по каждому
'''

params = {'v':'5.131',
          'access_token':access_token,
          'user_id': user_id,
          }
# url = 'https://api.vk.com/method/friends.getOnline'
url = 'https://api.vk.com/method/groups.get'

response = requests.get(url, params = params).json()

#получаем список групп
groups = response['response']['items']
count = 0
for item in groups[:1]:
    url = 'https://api.vk.com/method/groups.getMembers'
    params = {'v':'5.131',
          'access_token':access_token,
          'group_id': item
           }
    response = requests.get(url, params = params).json()

    #получаем список пользователей в группе
    members = response['response']['items']
    for member in members:
        url = 'https://api.vk.com/method/users.get'
        params = {'v': '5.131',
                  'access_token': access_token,
                  'user_ids': member,
                  'fields': 'city,online'
                  }
        response = requests.get(url, params=params).json()

        #отображаем инфо о пользователе, если у него открытый аккаунт
        try:
            print(f'id: {response["response"][0]["id"]}, ФИО: {response["response"][0]["first_name"]}, {response["response"][0]["last_name"]}, '
              f'Город: {response["response"][0]["city"]["title"]}, Онлайн: {"да" if response["response"][0]["online"] == 1 else "нет"}')
        except Exception as e:
            print(e)
        count += 1
        if count % 5 == 0:
            time.sleep(5)
