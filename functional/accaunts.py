from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from functional.database import session, User
import requests


# user_pin1 = 22204199201225
user_pin2 = 22109199100358


def check_user_pin(user_pin):
    try:
        req = requests.get(f'http://10.232.10.51:8009/check-pin/{user_pin}/') #
        # req = requests.get(f'http://10.2.10.82:8000/check-pin/{user_pin}/') #
        if req.json()['id']:
            return req.json()['id']
    except KeyError:
        return False

# print(datetime.now())

# print(check_user_pin(user_pin2))
# res = check_user_pin(user_pin2)
# print(res[1])
user_pinn = 22109199100358
def coming_out(user_pin):
    req = requests.get(f'http://10.2.10.82:8000/coming_leaving/{user_pin}/')      # local
    # req = requests.get(f'http://10.232.10.51:8009/coming_leaving/{user_pin}/')  # server
    return True, req

# print(coming_out(user_pinn))


def id_org(qr_code_value):  # {'loc_width': '45', 'loc_length': '65'}
    try:
        req = requests.get(f'http://10.232.10.51:8009/check-loc/{qr_code_value}/')
        if req.json():
            return req.json()['loc_width'], req.json()['loc_length']
        else:
            return False
    except Exception:
        return False

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


def check_user_from_db(tg_id):
    see = session.query(User.tg_id).filter(User.tg_id == tg_id).all()
    # print(see)
    if see:
        return True#, see[0][0]
    else:
        return False


def get_user_pin_by_id(id):
    pin = session.query(User.user_pin).filter(User.tg_id == id).all()
    if pin:
        return pin[0][0], True
    else:
        return False, False


def pin_remake_by_id(id, user_pin): # Обновляется пин юзера по id
    query = session.query(User).filter(User.tg_id == id).first()
    if len(user_pin) == 14:
        try:
            query.user_pin = user_pin # ИНН от юзера приравнивается к пину в базе бота
            session.commit()
            return True
        except IntegrityError:
            session.rollback()  # откатываем session.update(User.user_pin)
            return False
    else:
        return False

# a = 466409778
# print(pin_create(a))
# print(get_user_pin_by_id(a))

def register_user(id, qr_code_value, phone, pin):
    user = User(tg_id=id, organization_id=qr_code_value, phone=phone, user_pin=pin)

    session.add(user)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False
