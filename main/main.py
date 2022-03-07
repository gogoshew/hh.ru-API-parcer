import requests
import json
import time
import os
from datetime import datetime


# Переменная для отслеживания текущей даты
current_date = datetime.now().strftime('%d_%m_%Y')

def get_page(page = 0):
    '''
    Создаем метод для получения страницы со списком вакансий
    page - Индекс страницы
    '''

    # Словарь параметров GET запроса
    params = {
        'text': 'Разработчик Python',
        'area': 1, #Поиск по вакансиям в Москве
        'page': page, #Индекс страницы
        'per_page': 100 # Количество вакансий на странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    # data = req.content.decode()
    req.close()
    return data

def get_pages(n):
    '''
    Создадим метод для считывания n страниц и записи результатов запроса в json
    n - параметр, определяющий сколько страниц будет обработано
    '''

    # Создаем папку для json файлов
    if not os.path.exists(f'data({current_date})'):
        os.mkdir(f'data({current_date})')

    for page in range(n):
        json_object = json.loads(get_page(page))

        with open(fr'data({current_date})/page({page + 1}).json', 'w', encoding='utf-8') as file:
            json.dump(json_object, file, indent=4, ensure_ascii=False)

        if json_object['pages'] - page <= 1:
            break

        # Определим небольшую паузу чтобы не словить блокировку от hh.ru
        time.sleep(0.25)

    print('Страницы собраны')

# Получим информацию по каждой вакансии
def get_vacancy_information():
    get_pages(20)

    # Создаем папку для вакансий
    if not os.path.exists(f'vacancies({current_date})'):
        os.mkdir(f'vacancies({current_date})')

    for page in os.listdir(fr'data({current_date})/'):
        with open(fr'data({current_date})/{page}', encoding='utf-8') as file:
            json_text = file.read()

    # Преобразуем текст в объект справочника
    json_object = json.loads(json_text)

    for vacancy in json_object['items']:

        req = requests.get(vacancy['url'])
        data = req.content.decode()
        req.close()

        # Создадим json файл с идентификатором вакансии
        with open(fr'vacancies({current_date})/{vacancy["id"]}).json', 'w', encoding='utf-8') as file:
            file.write(data)

        time.sleep(0.25)

    print('Вакансии собраны')


def main():
    get_vacancy_information()

if __name__ == '__main__':
    main()