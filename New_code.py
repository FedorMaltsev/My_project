#from openpyxl import *
import openpyxl

name_file = 'таблица_после_ереси'#input('Введите название файла: ')
# file_table = openpyxl.open(f'C:/Users/cheog/Desktop/{name_file}.xlsx', read_only=True).active
# table_list = [[file_table[i][j].value for j in range(0, file_table.max_column)] for i in range(1, file_table.max_row + 1)]
#
# for rows in table_list:
#     print(rows)

try:
    # with openpyxl.open(f'C:/Users/cheog/Desktop/{name_file}.xlsx', read_only=True).active as file_table:
    #     table_list = [[file_table[i][j].value for j in range(0, file_table.max_column)] for i in range(1, file_table.max_row + 1)]
    #     for rows in table_list:
    #         print(*rows)
    file_table = openpyxl.open(f'C:/Users/cheog/Desktop/{name_file}.xlsx', read_only=True).active
    table_list = [[str(file_table[i][j].value) for j in range(0, file_table.max_column)] for i in range(1, file_table.max_row + 1)]

    for rows in table_list[1:]:
        print(rows)

except Exception as ex:
    print('Такой файл не найден', ex)