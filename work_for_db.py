import psycopg2
from config import host, user, password, db_name
import os
from main import name_table_1, name_table_2

def select_all(selected_table):                 #Вывод всей базы
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT *
            FROM {selected_table}
            """
        )
        for row in cursor.fetchall():
            print(*row)

def select_one(selected_table):        #Вывод по одному конкретному полю (определённая сводка)
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

def for_change_value(selected_table, name_columns): # Во избежание дублирования кода, функция для change_value
    for key in name_columns:
        new_elem = input(
            f'Нажмите ENTR, чтобы оставить старое значение. Перезапись {key}, введите новое значение/информацию: ').strip()
        if new_elem != '':  # Вводим пустую строку, если хотим оставить старое значение
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE {selected_table}
                    set {key} = {new_elem}
                    where {selected_table}.number = {id}
                    """
                )
                for row in cursor.fetchall():
                    print(f'Изменения внесены, текущая запись: {row}')

def change_value(selected_table): # Изменение поля по номеру легиона
    try:
        id = input('Введите номер легиона: ')

        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         f"""
        #         SELECT *
        #         FROM {selected_table}
        #         where {selected_table} = {id}
        #         """
        #     )
        #     for row in cursor.fetchall():
        #         print(f'Выбрана запись: {row}')
        #     old_value = cursor.fetchall()  # ВНИМАНИЕ СЮДА, изменение параметров с использованием старых
        # new_value = { 'name_order' : old_value[0], 'name_primarch' : old_value[1], 'date_of_found' : old_value[3], 'loyalty' : old_value[4], 'number' : old_value[5], 'home_world' : old_value[6] }
        # for key in new_value.keys():
        name_columns_after_heresy = ('name_order', 'name_primarch', 'date_of_found', 'loyalty', 'number', 'home_world')
        name_columns_before_heresy = ('name_order', 'number')
        if selected_table == name_table_1: # В зависимости от того, какая таблица выбрана основной
            for_change_value(selected_table, name_columns_after_heresy)
        else:
            for_change_value(selected_table, name_columns_before_heresy)

    except:
        print('чел...')


def insert_value_after_heresy(selected_table): # Добавление топорное, требуется куча проверок полей, пока добавит только верные данные
    try:
        print('Если данные отсутствуют - вводите null')
        name_order = input('Введите имя ордена (name_order):' )
        name_primarch = input('Введите имя примарха (name_primarch): ' )
        date_of_found = input('Введите дату основания в формате dd.mm.yyyy (date_of_found): ' )
        loyalty = input('Введите статус лояльности (loyalty): true/false ' )
        number = input('Введите уникальный номер легиона (number): ' )
        home_world = input('Введите родной мир или основную базу (home_world): ' )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT into {selected_table}
                values (
                        {name_order}, 
                        {name_primarch}, 
                        {f"TO_DATE('{date_of_found}', 'dd.mm.yyyy')" if date_of_found != 'null' else 'null::timestamp'},
                        {loyalty if loyalty.lower() != 'null' else 'null::boolean'},
                        {number},
                        {home_world}
                        )
                """
            )
            for row in cursor.fetchall():
                print(row)
    except:
        print('чел...')


def insert_value_before_heresy(selected_table): # Добавление топорное, требуется куча проверок полей, пока добавит только верные данные
    try:
        print('Если данные отсутствуют - вводите null')
        name_order = input('Введите имя ордена (name_order):' )
        number = input('Введите уникальный номер легиона (number): ' )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT into {selected_table}
                values (
                        {name_order}, 
                        {number}
                        )
                """
            )
            for row in cursor.fetchall():
                print(row)
    except:
        print('чел...')





def swap(name_1, name_2, selected_table): # Переключает на другую таблицу
    if name_1 == selected_table:
        return name_2
    else:
        return name_1


try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # os.system('python main.py') # Считать нужные файлы эксель, открыть и заполнить таблицы
    print('Здесь будет проводиться работа с таблицей.')
    selected_table = name_table_1
    swith_dict = { 1 : select_all, 2 : select_one, 3 : change_value, 4 : insert_value_after_heresy if selected_table == name_table_1 else insert_value_before_heresy, 5 : 5, 6 : 6, 7 : 7, 8 : 8, 9 : 9 }
    while True:
        try:
            print('Архив Империума выполнит ваш запрос. Или вызовет стражей.')
            print(f"""          1 - вывести весь архив\n
            2 - вывести определенную сводку\n
            3 - изменить запись в архиве\n
            4 - добавить новую запись в архив\n
            5 - удалить запись из архива\n
            6 - увидеть изменения в названих легионов за 10 веков\n
            7 - вывести всю историю\n
            8 - переключить на архив {name_table_2 if selected_table == name_table_1 else name_table_1}\n
            9 - закрыть архив""")
            command = int(input())
            if command == 8:
                selected_table = swap(name_table_1, name_table_2, selected_table)
            else:
                swith_dict[command](selected_table)

        except Exception as ex:
            print(ex, '\nМоя ошибка не повод ругаться, лучше помоги мне стать лучше')
except Exception as ex:
    print('Всё плохо, потому что ', ex)

finally:
    if connection:
        connection.close()
        print('Форточка закрыта')