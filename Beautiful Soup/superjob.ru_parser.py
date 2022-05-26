#https://www.superjob.ru/vacancy/search/
#?keywords=Python&geo%5Bc%5D%5B0%5D=10&geo%5Bc%5D%5B1%5D=1

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os

pages_count = 0

main_url = 'https://www.superjob.ru'
params = {"keywords": "Python",
          "geo%5Bc%5D%5B0%5D": "10",
          "geo%5Bc%5D%5B1%5D=1": "1"}
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/101.0.4951.67 Safari/537.36"}

link = main_url + "/vacancy/search"
next_page_link = True
vacancy_info_result = []

def parce_vac_from_page(page):

    """
    считаывает сохраненные html страницы  и парсит оттуда данные
    """

    soup = bs(page, "html.parser")

    div_with_vac = soup.findAll("div", class_="f-test-vacancy-item")

    for item in div_with_vac:
        vacancy_info = {}
        vac_anchor = item.findChildren(recursive=False)[0].findChildren(recursive=False)[2]
        vacancy_info["name"] = vac_anchor.find_all('span')[0].find('a').getText()
        vacancy_info["link"] = main_url + vac_anchor.find_all('span')[0].find('a').get('href', 'None')

        salary = vac_anchor.find('span', 'f-test-text-company-item-salary').getText()
        if salary != 'По договоренности':

            if "—" in salary:
                vacancy_info['salary_min'] = int(salary.split("—")[0].replace("\xa0", ''))
                salary_max_currency = salary.split("—")[1].split("\xa0")
                vacancy_info['currency'] = salary_max_currency.pop(-1)
                vacancy_info['salary_max'] = int("".join(salary_max_currency))

            elif "от" in salary:
                salary_min_currency = salary.split('\xa0')
                vacancy_info['currency'] = salary_min_currency.pop(-1)
                vacancy_info['salary_min'] = int("".join(salary_min_currency[1:]))
                vacancy_info['salary_max'] = None

            elif "до" in salary:
                salary_max_currency = salary.split('\xa0')
                vacancy_info['currency'] = salary_max_currency.pop(-1)
                vacancy_info['salary_max'] = int("".join(salary_min_currency[1:]))
                vacancy_info["salary_min"] = None

        else:
            vacancy_info['currency'] = None
            vacancy_info['salary_max'] = None
            vacancy_info["salary_min"] = None
        try:
            vacancy_info["company_name"] = vac_anchor.find('span', 'f-test-text-vacancy-item-company-name').getText()
        except Exception:
            vacancy_info["company_name"] = None
        try:
            vacancy_info['location'] = vac_anchor.find('span', 'f-test-text-company-item-location').getText()

        except Exception:
            vacancy_info["location"] = None
        try:
            vacancy_info['feature'] = vac_anchor.parent.find('span', 'f-test-badge').getText()
        except Exception:
            vacancy_info['feature'] = None

        vacancy_info_result.append(vacancy_info)

def parce_all_pages(link, pages_count):

    """
    - принимает ссылку на страницу, сохраняет в файл html
    - ищет на странице кнопку дальше
    - если находит берет с неё ссылку и возвращает
    - если нет - возвращает None
    - чтобы не дергать сайт постоянно 1 раз скачиваем себе файл с каждой страницей и сохраняем
    """
    if os.path.exists(f'superjob_page_{pages_count}.html'):
        print(f'Страница {pages_count} уже скачана')
    else:
        try:
            if pages_count == 0:
                response = requests.get(link, params=params, headers=headers)
            else:
                response = requests.get(link)
            with open(f'superjob_page_{pages_count}.html', "w", encoding='utf-8') as f:
                f.write(response.text)
        except Exception:
            print("Ошибка")

    with open(f'superjob_page_{pages_count}.html', "r", encoding='utf-8') as f:
        page = f.read()
        parce_vac_from_page(page=page)

    soup = bs(page, "html.parser")

    active_btn = soup.find('a', class_="f-test-button_active")

    next_page = active_btn.parent.find_all('a')[-1]

    if next_page.text == 'Дальше':
        return main_url + next_page.get('href')
    return None

while link:
    link = parce_all_pages(link = link,
                            pages_count = pages_count)
    pages_count += 1




result = pd.DataFrame(vacancy_info_result)[['name', 'company_name', 'location',
                                         'salary_min', 'salary_max', 'currency',
                                         "feature", 'link']]
print(result)


