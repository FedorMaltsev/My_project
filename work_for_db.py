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

def for_select_one(selected_table, column, value): # Вынесено в отдельную функцию (эту), так как пригодится в других
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT *
            FROM {selected_table}
            where {column} = {value}
            """
        )
        return cursor.fetchall()

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
            ind = int(input())
        else:
            print(f"""  1 - name_order
                        2 - number""")
            ind = int(input())  # Находится здесь, так как разная проверка на корректность

        column = { 1 : 'name_order', 2 : 'number', 3 : 'date_of_found', 4 : 'loyalty', 5 : 'name_primarch', 6 : 'home_world' }
        value = input(f'Введите значение {column[ind]}: ')
        for row in for_select_one(selected_table, column[ind], value):
            print(row)
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         f"""
        #         SELECT *
        #         FROM {selected_table}
        #         where {column[ind]} = {value}
        #         """
        #     )
        #     for row in cursor.fetchall():
        #         print(row)
    except Exception as ex:
        print(ex, '\nМоя ошибка не повод ругаться, лучше помоги мне стать лучше')

def for_change_value(selected_table, name_columns, number): # Во избежание дублирования кода, функция для change_value
    old_values_tuple = for_select_one(selected_table, 'number', number)[0] # Кортеж со старыми значениями, для удобства пользователя. [0] нужен из-за того, что cursor.fetchall() возвращает список кортежей
    old_values_dict = { name_columns[i] : str(old_values_tuple[i]) for i in range(0, len(name_columns)) } # Приходится идти таким путём, чтобы не вызывать select на каждой итерации
    for key in name_columns:
        new_elem = input(
            f'Перезапись {key}, нажмите ENTR, чтобы оставить значение {old_values_dict[key]}. Введите новое значение/информацию: ').strip()
        if new_elem != '':  # Вводим пустую строку, если хотим оставить старое значение
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE {selected_table}
                    set {key} = {new_elem}
                    where {selected_table}.number = {number}
                    """
                )
                for row in cursor.fetchall():
                    print(f'Изменения внесены, текущая запись: {row}')

def change_value(selected_table): # Изменение поля по номеру легиона
    try:
        number = input('Введите номер легиона: ')

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
            for_change_value(selected_table, name_columns_after_heresy, number)
        else:
            for_change_value(selected_table, name_columns_before_heresy, number)

    except Exception as ex:
        print(ex, '\nМоя ошибка не повод ругаться, лучше помоги мне стать лучше')


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





def swap(name_1, name_2, selected_table): # Для переключения на другую таблицу
    if name_1 == selected_table:
        print(f'Выбран архив {name_2}')
        return name_2
    else:
        print(f'Выбран архив {name_1}')
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
    swith_dict = { 1 : select_all, 2 : select_one, 3 : change_value, 4 : insert_value_after_heresy if selected_table == name_table_1 else insert_value_before_heresy, 5 : 5, 6 : 6, 7 : 7, 9 : 9 }
    while True:
        try:
            print('Архив Империума выполнит ваш запрос. Или вызовет стражей.')
            print(f"""             
            1 - вывести весь архив
            2 - вывести определенную сводку
            3 - изменить запись в архиве
            4 - добавить новую запись в архив
            5 - удалить запись из архива
            6 - увидеть изменения в названих легионов за 10 веков
            7 - вывести всю историю
            8 - переключить на архив {name_table_2 if selected_table == name_table_1 else name_table_1}
            9 - закрыть архив""")
            command = int(input())
            if command in (1, 2, 3, 4, 5, 6, 7):
                swith_dict[command](selected_table)
            elif command == 8:
                selected_table = swap(name_table_1, name_table_2, selected_table)
            elif command == 9:
                print('Работа завершена, архив закрыт')
                break

        except Exception as ex:
            print(ex, '\nМоя ошибка не повод ругаться, лучше помоги мне стать лучше')
except Exception as ex:
    print('Всё плохо, потому что ', ex)

finally:
    if connection:
        connection.close()
        print('Форточка закрыта')