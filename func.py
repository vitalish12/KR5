import math
import psycopg2
import requests
from config import config
from typing import Any

#параметры подключения к БД
params = config()

#id работодателей
id=2733062, 701365, 864086, 598471, 1519234, 5971349, 9261916, 3361389, 5202841, 67611

def get_hh_vacancies(id: str) -> list:
    '''парсинг вакансий от 10 работодателей через API HH'''
    #получаем количество страниц с вакансиями (по 100 на каждой странице)
    print('Идёт загрузка данных. Это может занять какое-то время')
    response = requests.get(f"https://api.hh.ru/vacancies?", params={'employer_id': {id}, 'per_page': 1, 'page': 1})
    count_vacancies = response.json()['found']
    count_page = math.ceil(count_vacancies / 100)

    #делаем запрос с использованием количества страниц
    data_requests = []
    for page in range(count_page):
        response = requests.get(f"https://api.hh.ru/vacancies?", params={'employer_id': {id}, 'per_page': 100, 'page': page})
        datas = response.json()['items']
        for data in datas:
            data_requests.append([data['employer']['id'],
                                  data['employer']['name'],
                                  data['name'],
                                  data['alternate_url'],
                                  data['salary']['from'] if data['salary'] is not None else None,
                                  data['salary']['to'] if data['salary'] is not None else None,
                                  data['salary']['currency'] if data['salary'] is not None else None])
    return data_requests
    print(f'Загрузка данных о вакансиях от {len(id)} работодателей завершена')


def convert_sql():
    '''конвертирует .sql файл в .py для ипользования запросов'''
    with open('queries.sql') as old, open ('queries.py', 'w') as new:
        a = old.readlines()
        for d in a:
            if '--' not in d:
                new.writelines(d)


def create_database(database_name: str, params: dict) -> None:
    '''создаёт базу данных и таблицу для наполнения данными из API запроса'''
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE employers (
                employer_id int,
                employer_name varchar (50) NOT NULL,
                vacancy_name varchar (100) NOT NULL,
                url text,
                salary_from int,
                salary_to int,
                currency varchar (50))
        ''')
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    '''сохранение данных из запроса API HH в таблицу базы данных'''
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for i in data:
            cur.execute('INSERT INTO employers VALUES (%s, %s, %s, %s, %s, %s, %s)', i)

    conn.commit()
    conn.close()


convert_sql()