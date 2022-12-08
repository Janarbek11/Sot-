import os, glob
import pathlib
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import accaunts
import face_controll
import location as geolocation
import qr
from keyboards import *
from accaunts import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import Token
from aiogram.dispatcher import FSMContext


storage = MemoryStorage()
bot = Bot(Token)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    id_in_qr = State()
    pin = State()
    phone = State()
    photo = State()


@dp.message_handler(commands=['start'])
async def user_register(message: types.Message):
    await message.answer("Отправьте фото QR-кода находящийся в вашей организации")
    @dp.message_handler(content_types=['photo'])
    async def get_photo(message: ContentType.PHOTO, state: FSMContext):
        file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
        id = file_info.file_path
        qr_photo = (await bot.download_file(id,
                                            f'/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/data/{message.from_user.id}{message.date}.png'))
        filename = pathlib.Path(f'{message.from_user.id}{message.date}.png')
        qr_code_value = qr.read_qr_code(f'data/{filename.name}')
        res_org = accaunts.id_org(qr_code_value)
        for file in glob.glob("data/*"):
            os.remove(file)
        await state.update_data(id_in_qr=res_org)
        await message.answer('Теперь введите ваш ИНН.')
        await UserState.pin.set()


@dp.message_handler(state=UserState.pin)
async def get_user_pin(message: types.Message, state: FSMContext):
    await state.update_data(pin=message.text)
    data = await state.get_data()
    user_pin = data['pin']
    if len(user_pin) == 14:
        result = accaunts.cheсk_user_pin(user_pin)
        if result:
            await bot.send_message(message.from_user.id, 'Ваш пин имеется в базе данных')
            await message.answer('Отправьте номер вашего телефона.', reply_markup=number_key())
            await state.finish()
        else:
            await message.answer('Не найден')
            await state.finish()
            await UserState.pin.set()
    else:
        await message.answer('Некорректно ввели ИНН.\nВведите еще раз.')
        await state.finish()
        await UserState.pin.set()


@dp.message_handler(content_types=['contact'])
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    # здесь data нужно сохранить в базу данных
    await message.answer(f'contact: {data["phone"]}')
    await state.finish()
    await message.answer('Отправьте фотографию вашего лица для идентификации.')


@dp.message_handler(content_types=['photo'])
async def get_phone(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    file = await bot.get_file(file_info.file_id)
    id = file_info.file_path
    face_photo = (await bot.download_file(id,
                                          f'/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/faces/{message.from_user.id}.jpg'))
    img1 = pathlib.Path(f'{message.from_user.id}.jpg')
    face_read = face_controll.photo_identificate(
        f'/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/faces/{img1.name}')
    if face_read == True:
        await bot.send_message(message.from_user.id, 'Классно Вы прошли идентификацию')
    elif face_read != False:
        await bot.send_message(message.from_user.id, 'Хмм... \nНе похож на Вас', reply_markup=menu_key())



@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message, state: FSMContext):
    user_loc = message.location.latitude, message.location.longitude
    data = await state.get_data()
    res = geolocation.ras(user_loc, data['id_in_qr'])
    if res > 200:
        await message.answer('Вы еще не дощли до работы', reply_markup=menu_key())
    else:
        await message.answer(f'{res} m', reply_markup=types.ReplyKeyboardRemove())
    for file in glob.glob(f"data/{message.from_user.id}{message.date}.png"):
        os.remove(file)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
