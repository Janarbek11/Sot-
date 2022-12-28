from aiogram.types import CallbackQuery, ContentType, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def check_by_tg_id():
    btn_check = KeyboardButton('Проверить')
    btn_not_check = KeyboardButton('Не проверять')
    btn_id = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_check).add(btn_not_check)
    return btn_id


def location_key():
    btn = KeyboardButton('🕹 Отправить местоположение', request_location=True)
    btnLocation = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return btnLocation


def name_check():
    btn_yes = KeyboardButton('Да')
    btn_no = KeyboardButton('Нет')
    btn = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_yes).add(btn_no)
    return btn


def go_home():
    btn_home = KeyboardButton('Я домой🏡')
    btn_home1 = KeyboardButton('Я собираюсь уходить🚶🏻')
    btn = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_home)
    btn1 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_home1)
    return btn, btn1


def number_key():
    btn = KeyboardButton('Отправить номер', request_contact=True)
    btnLocation = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return btnLocation


def registration_key():
    btn = KeyboardButton('Пройти регистрацию')
    btnReg = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return btnReg



