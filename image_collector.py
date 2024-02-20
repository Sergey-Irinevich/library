import requests as rs
from bs4 import BeautifulSoup


def get_images(url):
    HEADERS = {'User-agent': 'Chrome/85.0.4183.121',
               'Accept-Language': 'en',
               'accept': '*/*',
               'origin': 'https://megamarket.ru',
               'sec-fetch-site': 'cross-site',
               'sec-fetch-mode': 'cors',
               'sec-fetch-dest': 'empty',
               'referer': 'https://megamarket.ru',
               'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
    response = rs.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('picture', class_='product-picture')

    found = []
    for item in items:
        found.append(item.find('img').get('data-srcset'))

    return found


found_all = []  # список ссылок на картинки
for i in range(2, 27):
    found_all += get_images(f'https://www.chitai-gorod.ru/catalog/books/klassicheskaya-proza-110003?page={i}')

for i in range(1, len(found_all) + 1):
    resp = rs.get(found_all[i-1])
    filename = f'dataset\\{i}.jpg'
    fl = open(filename, 'wb')  # открыть файл
    fl.write(resp.content)  # записать в него картинку
    fl.close()
