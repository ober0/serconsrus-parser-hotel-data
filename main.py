import json

import time
from bs4 import BeautifulSoup
import requests
import lxml

headers = {
    'Accept':'*/*',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
}

main_url = 'https://www.serconsrus.ru/faq/federalnyj-perechen-gostinicy/?PAGEN_1='
code = 200
src_all = []
value_json = []
ind = 0

page_for_parse = int(input('Сколько страниц парсим?(max-360) >>>'))
if page_for_parse > 360:
    page_for_parse = 360

start = time.time()
for page in range(page_for_parse):
    url = f'https://www.serconsrus.ru/faq/federalnyj-perechen-gostinicy/?PAGEN_1={page}'
    req = requests.get(url, headers=headers)
    code = req.status_code
    if code == 200:
        soup = BeautifulSoup(req.text, 'lxml')
        print(f'page {page} success parsed')
        all_table = soup.find('div', class_='psevdo-table-body').find_all('div', class_='psevdo-table-tr')
        table_ins = 0
        for table in all_table:
            table_ins += 1
            try:
                src = table.find('a', class_='ajax-link')['href']
                src_all.append(src)
            except:
                print(f'''   table {table_ins} not success''')
    else:
        print(f'page {page} not success')


for src in src_all:
    ind += 1
    try:
        url = f'https://www.serconsrus.ru/faq/federalnyj-perechen-gostinicy/{src}'
        req = requests.get(url, headers=headers)

        soup = BeautifulSoup(req.text, 'lxml')

        table = soup.find('table', class_='border-normal')
        all_data = table.find_all('tr')
        all_data = all_data[1:]

        json_structure = {
        }
        for column in all_data:
            all_td = column.find_all('td')
            description = all_td[0].find('b').text
            value = all_td[1].text
            try:
                json_structure[description] = value
            except:
                json_structure[description] = 'No value'
        print(f'Запись {ind} Завершена')
    except:
        print(f'Запись {ind}  не Завершена')

    value_json.append(json_structure)

with open("data.json", "w", encoding='utf-8') as json_file:
    json.dump(value_json, json_file, indent=4, ensure_ascii=False)

time_end = time.time()

print('Процесс завершен')
print(f'Было затраченно {time_end - start} секунд')






