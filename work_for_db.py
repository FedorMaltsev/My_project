import psycopg2
from config import host, user, password, db_name

def select_all():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM after_the_heresy
            """
        )
        for row in cursor.fetchall():
            print(*row)

def select_one():
    try:
        row, value = input('Имя поля: '), input('Значение поля: ')
        if row not in ('name_order', 'name_primarch', 'date_of_found', 'loyalty', 'number', 'home_world'):
            0 / 0 #  Да, это костыльный способ не дать пройти некорректному названию поля
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM after_the_heresy
                where {row} = {value}
                """
            )
            for row in cursor.fetchall():
                print(row)
    except:
        print('чел...')

def insert_value(): # Добавление топорное, требуется куча проверок полей, пока добавит только верные данные
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
                INSERT into after_the_heresy
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

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    print('Здесь будет проводиться работа с таблицей.')
    swith_dict = { 1 : select_all, 2 : select_one, 3 : 3, 4 : 4, 5 : 5 }
    while True:
        try:
            print('Архив Империума выполнит ваш запрос. Или вызовет стражей.')
            print('1 - вывести весь архив\n2 - вывести определенную сводку\n3 - вывод по особым условиям\n4 - добавить новую запись в архив\n5 - удалить запись из архива')
            command = int(input())
            swith_dict[command]()

        except Exception as ex:
            print(ex, '\nМоя ошибка не повод ругаться, лучше помоги мне стать лучше')
except Exception as ex:
    print('Всё плохо, потому что ', ex)

finally:
    if connection:
        connection.close()
        print('Форточка закрыта')