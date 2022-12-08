from aiogram.types import CallbackQuery, ContentType, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def menu_key():
    btn_face = KeyboardButton('Отправить фото лица')
    btn_qr = KeyboardButton('Отправить фото QR-code')
    btn_in_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_face).add(btn_qr)
    return btn_in_menu


def location_key():
    btn = KeyboardButton('🕹 Отправить местоположение', request_location=True)
    btnLocation = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return btnLocation


def number_key():
    btn = KeyboardButton('Отправить номер', request_contact=True)
    btnLocation = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return btnLocation


def registration_key():
    btn = KeyboardButton('Пройти регистрацию')
    btnReg = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    return btnReg



