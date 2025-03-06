#from openpyxl import *
import openpyxl
import psycopg2
from config import host, user, password, db_name
import os
from main import name_table_1, name_table_2
print('PYYYYYYYYYYYYYSSSSSSSKKKKKKAAAAAAAAA')

def select_one(selected_table):
    try:
        print('По какому аргументу вам нужна сводка?')
        if selected_table == name_table_1:
            print(f"""  1 - name_order
                        2 - number
                        3 - date_of_found
                        4 - loyalty
                        5 - name_primarch
                        6 - home_world""")
            ind = input()
        else:
            print(f"""  1 - name_order
                        2 - number""")
            ind = input() # Находится здесь, так как разная проверка на корректность

        column = { 1 : 'name_order', 2 : 'number', 3 : 'date_of_found', 4 : 'loyalty', 5 : 'name_primarch', 6 : 'home_world' }
        value = input(f'Введите значение {column[ind]}: ')
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM {selected_table}
                where {column[ind]} = {value}
                """
            )
            for row in cursor.fetchall():
                print(row)
    except:
        print('чел...')

connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
connection.autocommit = True