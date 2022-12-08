import sqlite3
import requests
import json


# def reg_user(user_id, organization_id):
#     req = 'http://127.0.0.1:8002/users/'
#     json = {'user_id': user_id, 'organization_id': organization_id}
#     x = requests.post(req, json=json)
#     print(x.json())
# reg_user(123, 5555)

# user_pin = 22204199201225
# user_pin = 22204199201226


def cheсk_user_pin(user_pin):
    req = requests.get(f'http://10.232.10.51:8009/check-pin/{user_pin}/') #
    try:
        if req.json():
            return req.json()['id']
    except:
        if req.json() == {'message': 'error'}:
            return False


def id_org(qr_code_value):  # {'loc_width': '45', 'loc_length': '65'}
    req = requests.get(f'http://10.232.10.51:8009/check-loc/{qr_code_value}/')
    if req.json():
        return req.json()['loc_width'], req.json()['loc_length']
    else:
        return False


# print(cheсk_user_pin(user_pin))

# print(id_org(7))

# location api   http://10.232.10.51:8009/check-loc/{id}/  {width: 675, lengt: 56789} string


# Преобразование данных в двоичный формат
# def convert_to_binary_data(filename):
#     with open(filename, 'rb') as file:
#         blob_data = file.read()
#     return blob_data
#
#
# # Добавление фотоографии в БД
# def insert_user_photo(photo):
#     try:
#         con = sqlite3.connect('accaunts.db')
#         cur = con.cursor()
#         print("Подключен к SQLite")
#
#         insert_query = """INSERT INTO users(user_photo) VALUES (?)"""
#
#         emp_photo = convert_to_binary_data(photo)
#         # Преобразование данных в формат кортежа
#         data_tuple = (emp_photo,)
#         cur.execute(insert_query, data_tuple)
#         con.commit()
#         print("Изображение успешно вставлен как BLOB в таблицу")
#         cur.close()
#
#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#     finally:
#         if con:
#             con.close()
#             print("Соединение с SQLite закрыто")


# insert_user_photo("jake2.jpg")

