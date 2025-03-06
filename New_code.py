#from openpyxl import *
import openpyxl
import psycopg2
from config import host, user, password, db_name
import os
from main import name_table_1, name_table_2
print('PYYYYYYYYYYYYYSSSSSSSKKKKKKAAAAAAAAA')

def select_one(selected_table):
    try:
        row, value = input('Имя поля: '), input('Значение поля: ')
        if row not in ('name_order', 'name_primarch', 'date_of_found', 'loyalty', 'number', 'home_world'):
            0 / 0 #  Да, это костыльный способ не дать пройти некорректному названию поля
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM {selected_table}
                where {row} = {value}
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