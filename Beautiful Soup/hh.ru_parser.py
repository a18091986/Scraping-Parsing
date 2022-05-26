# https://hh.ru/search/vacancy?text=python+junior&salary=&clusters=true&area=1&ored_clusters=true&enable_snippets=true

'''
https://hh.ru/search/vacancy?
text=Data+analyst+%7C+data+scientist+%7C+Data+Engineer&
from=suggest_post&
salary=&
clusters=true&
area=1&area=1217&area=232&area=113&area=2&
ored_clusters=true&
enable_snippets=true
'''

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os

pages_count = 0

main_url = 'https://hh.ru'
params = {"text": "Data Analyst | Data Engineer | Data Scientist",
          "from": "suggest_post",
          "clusters": "true",
          "area": "113",
          "ored_clusters": "true",
          "enable_snippets": "true"}
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/101.0.4951.67 Safari/537.36"}

link = main_url + "/search/vacancy"

next_page_link = True
vacancy_info_result = []


def parce_all_pages(link, pages_count):
    """
    - принимает ссылку на страницу, сохраняет в файл html
    - ищет на странице кнопку дальше
    - если находит берет с неё ссылку и возвращает
    - если нет - возвращает None
    - чтобы не дергать сайт постоянно 1 раз скачиваем себе файл с каждой страницей и сохраняем
    """
    if os.path.exists(f'head_hunter_page_{pages_count}.html'):
        pass
    else:
        try:
            if pages_count == 0:
                response = requests.get(link, params=params, headers=headers)
            else:
                response = requests.get(link, headers=headers)
            with open(f'head_hunter_page_{pages_count}.html', "w", encoding='utf-8') as f:
                f.write(response.text)
        except Exception:
            print("Ошибка")

    with open(f'head_hunter_page_{pages_count}.html', "r", encoding='utf-8') as f:
        page = f.read()
        parce_vac_from_page(page=page)

    soup = bs(page, "html.parser")

    btn_next = soup.find(attrs={"data-qa": "pager-next"})
    if btn_next:
        return main_url + btn_next.get('href')
    return None


def parce_vac_from_page(page):
    """
    считаывает сохраненные html страницы  и парсит оттуда данные
    """

    soup = bs(page, "html.parser")

    div_with_vac = soup.findAll("div", class_="vacancy-serp-item")

    for item in div_with_vac:
        vacancy_info = {}
        vacancy_info["name"] = item.find('a', attrs={"data-qa": 'vacancy-serp__vacancy-title'}).getText()
        vacancy_info["link"] = item.find('a', attrs={"data-qa": 'vacancy-serp__vacancy-title'})['href']

        salary = item.find('span', attrs={"data-qa": 'vacancy-serp__vacancy-compensation'})

        if salary:

            salary = item.find('span', attrs={"data-qa": 'vacancy-serp__vacancy-compensation'}).getText()

            if "–" in salary:
                salary = salary.split(' ')
                vacancy_info["salary_min"] = int(salary[0].replace("\u202f", ''))
                vacancy_info["salary_max"] = int(salary[2].replace("\u202f", ''))
                vacancy_info["currency"] = salary[3]

            elif "от" in salary:
                salary = salary.split(' ')
                vacancy_info['currency'] = salary[2]
                vacancy_info['salary_min'] = int(salary[1].replace("\u202f", ''))
                vacancy_info['salary_max'] = None

            elif "до" in salary:
                salary = salary.split(' ')
                vacancy_info['currency'] = salary[2]
                vacancy_info['salary_max'] = int(salary[1].replace("\u202f", ''))
                vacancy_info["salary_min"] = None

        else:
            vacancy_info['currency'] = None
            vacancy_info['salary_max'] = None
            vacancy_info["salary_min"] = None

        try:
            vacancy_info["company_name"] = item.find('a', attrs={"data-qa": 'vacancy-serp__vacancy-employer'}).getText()
        except Exception:
            vacancy_info["company_name"] = None
        try:
            vacancy_info["location"] = item.find('div', attrs={"data-qa": 'vacancy-serp__vacancy-address'}).getText()
        except Exception:
            vacancy_info["location"] = None
        try:
            if item.find('div', class_="search-result-label"):
                vacancy_info['feature'] = item.find('div', class_="search-result-label").getText()
            if item.find('div', class_="search-result-label_no-resume"):
                vacancy_info['feature'] = item.find('div', class_="search-result-label_no-resume").getText()
        except Exception:
            vacancy_info['feature'] = None

        vacancy_info_result.append(vacancy_info)


while link:
    link = parce_all_pages(link=link,
                           pages_count=pages_count)
    pages_count += 1

result = pd.DataFrame(vacancy_info_result)[['name', 'company_name', 'location',
                                            'salary_min', 'salary_max', 'currency',
                                            "feature", 'link']]
print(result)
