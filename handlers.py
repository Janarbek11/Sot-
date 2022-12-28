import datetime
import glob
import pathlib
import time

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from functional.accaunts import *
from functional.face_controll import *
from functional.location import *
from functional.qr import *
from functional.keyboards import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from functional.config import Token
from aiogram.dispatcher import FSMContext


storage = MemoryStorage()
bot = Bot(Token)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    updatePin = State()
    search_pin = State()
    location = State()
    start = State()
    registration = State()
    come2office = State()
    pin = State()
    phone = State()
    photo = State()

    freeze = State()


delta = 0       # Для ограничения по времени и обработки сообщений


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await message.answer(f"Здраствуйте, {message.from_user.last_name}!")
    await message.answer("Отправьте фото QR-кода находящийся в вашей организации")


@dp.message_handler(state=UserState.start)
async def start(message: types.Message, state: FSMContext):
    if message.text == 'Проверить':
        await message.answer('Проверяем ...', reply_markup=types.ReplyKeyboardRemove())
        check_user = check_user_from_db(message.from_user.id)
        await state.update_data(check_user=check_user)
        if not check_user:
            await message.answer('Вас нет в базе данных. Пройдите регистрацию.')
            await message.answer('Для этого введите ваш ИНН.')
            await UserState.pin.set()
        if check_user:
            await message.answer('В ответ на это сообщение отправьте любое слово🙂')
            await UserState.registration.set()
        # await message.answer('Отправьте фото вашего лица для идентификации.')
        # await UserState.photo.set()
    else:
        await message.answer('Я не могу поверить без разрешения пользователя! ')
        await state.finish()



@dp.message_handler(content_types=['photo'])
async def save_qr_code_photo(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    await bot.download_file(file_info.file_path, f'/home/janarbek/Рабочий стол/dipl/QR-Scanner-Bot/data/{message.from_user.id}{message.date}.png')
    filename = pathlib.Path(f'{message.from_user.id}{message.date}.png')
    qr_code_value = read_qr_code(f'data/{filename.name}')
    if qr_code_value:
        try:
            qr_code_value = int(qr_code_value)
            await state.update_data(qr_code_value=qr_code_value)
            res_org = id_org(qr_code_value)
            await state.update_data(id_in_qr=res_org)
            if not res_org:
                await message.answer('Вас еще нет в базе вашей организации')
                await state.finish()
            for file in glob.glob("data/*"):
                os.remove(file)
            await message.answer("Вас нужно проверить в базе, для этого нужно просто ответить данному сообщению)",
                                                        reply_markup=check_by_tg_id())
            await UserState.start.set()
        except Exception:
            await message.answer('Этот QR-код не действителен')
            await state.finish()
    if not qr_code_value:
        await message.answer('Ошибка при считывании QR-кода.')
        await state.finish()


@dp.message_handler(state=UserState.registration)
async def user_register(message: types.Message, state: FSMContext):
    check_user = check_user_from_db(message.from_user.id)
    if check_user:
        await bot.send_message(message.from_user.id, "Теперь отправьте ваше местоположение📍", reply_markup=location_key())
        await UserState.location.set()
    elif not check_user:
        data = await state.get_data()
        await message.answer('Идет сохранение в базу данных🔄')
        create_user = accaunts.register_user(message.from_user.id, data['qr_code_value'], data['phone'], data['pin'])
        if create_user:
            await message.answer("Вы зарегистрированы!✅\nОтправьте ваше местоположение📍", reply_markup=location_key())
            await UserState.location.set()
        if not create_user:
            await message.answer("Не удалось сохранить в базу данных. Попробуйте еще раз!")
            await state.finish()


@dp.message_handler(state=UserState.pin)
async def get_user_pin(message: types.Message, state: FSMContext):
    await state.update_data(pin=message.text)
    data = await state.get_data()
    user_pin = data['pin']
    if len(user_pin) == 14:
        result = accaunts.check_user_pin(user_pin)
        # chekqr and org id
        if result:
            await bot.send_message(message.from_user.id, 'Ваш пин имеется в базе данных🙌🏻')
            await message.answer('Отправьте номер вашего телефона📱', reply_markup=number_key())
            await UserState.phone.set()
        else:
            await message.answer('Не найден. Попробуйте все заново.')
            await state.finish()
    else:
        await message.answer('Некорректно ввели ИНН.\nВведите еще раз.')
        await UserState.pin.set()


@dp.message_handler(state=UserState.search_pin)
async def search_pin(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer('Замечательно)', reply_markup=types.ReplyKeyboardRemove())
        data = await state.get_data()
        result = data['result']
        org_id = data['qr_code_value']
        # chekqr and org id
        if result == org_id:
            await bot.send_message(message.from_user.id, 'Ваш пин имеется в базе данных🙌🏻')
            await message.answer('Отправьте номер вашего телефона📱', reply_markup=number_key())
            await UserState.phone.set()
        else:
            await message.answer('Не найден. Попробуйте все заново.')
            await state.finish()
    elif message.text == ' Нет':
        await message.answer('Введите ваш ИНН еще раз.')
        await UserState.pin.set()
    else:
        await message.answer('Попробуйте сначала🥴')
        await state.finish()


@dp.message_handler(state=UserState.phone, content_types=['contact'])
async def phone(message: types.Message, state: FSMContext):
    await message.reply('Сохраняю ваш номер.', reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Напиши что-нибудь')
    await UserState.registration.set()
    # await message.answer('Отправьте фотографию вашего лица для идентификации.')
    # await UserState.photo.set()



# @dp.message_handler(state=UserState.photo, content_types=['photo'])
# async def user_photo(message: types.Message, state: FSMContext):
#     file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
#     await bot.get_file(file_info.file_id)
#     await bot.download_file(file_info.file_path, f'{os.path.abspath("faces")}/{message.from_user.id}.jpg')
#     img = pathlib.Path(f'{message.from_user.id}.jpg')
#     # img2 = "Тут должен быть фото с АИС"
#     face_read = photo_identificate(
#         img=f'{os.path.abspath("faces")}/{img.name}',
#         pin=accaunts.get_user_pin_by_id(message.from_user.id)[0]
#     )
#     if face_read:
#         check_user = accaunts.get_user_pin_by_id(message.from_user.id)[1]   # there returned boolean
#         await state.update_data(check_user=check_user)
#         await bot.send_message(message.from_user.id, 'Классно! Вы прошли идентификацию!')
#         await UserState.registration.set()
#     elif not face_read:
#         await bot.send_message(message.from_user.id, 'Хмм... \nНе похож на Вас. Попробуйте еще раз.')
#         await UserState.photo.set()


@dp.message_handler(state=UserState.location, content_types=['location'])
async def handle_location(message: types.Message, state: FSMContext):
    user_loc1 = message.location.latitude
    user_loc2 = message.location.longitude
    data = await state.get_data()
    org_loc1 = data['id_in_qr'][0]
    org_loc2 = data['id_in_qr'][1]
    res = ras(user_loc1, user_loc2, org_loc1, org_loc2)
    if res > 200 or not res:
        await message.answer('Вы еще не дошли до работы👀\nПопробуйте заново как дойдете!👌🏻', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        to = datetime.now()
        await message.answer(f'Вы пришли на работу в {to.hour}:{to.minute} {to.day}-{to.month}-{to.year}👍🏻', reply_markup=types.ReplyKeyboardRemove())
        get_pin = accaunts.get_user_pin_by_id(message.from_user.id)
        # accaunts.coming_out(user_pin=get_pin[0])
        for file in glob.glob(f"data/{message.from_user.id}{message.date}.png"):
            os.remove(file)
        await message.answer('Дайте мне знак когда вы собираетесь уходить)', reply_markup=go_home()[1])
        await UserState.freeze.set()


@dp.message_handler(state=UserState.freeze)
async def freeze_time(message: types.Message, state: FSMContext):
    if datetime.now().hour < 12:
        await UserState.freeze.set()
    else:
        await message.answer('Вы домой?', reply_markup=go_home()[0])
        await state.finish()



@dp.message_handler(content_types = ['text'])
async def home(message: types.Message, state: FSMContext):
    if message.text == 'Я домой🏡' and datetime.now().hour > 13:
        get_pin = accaunts.get_user_pin_by_id(message.from_user.id)
        print(get_pin)
        await message.answer('Приятного отдыха!', reply_markup=types.ReplyKeyboardRemove())
        accaunts.coming_out(user_pin=get_pin[0])          # request на сервер где устанавливается время прихода
    else:
        await message.answer('Отправьте фото QR-кода.')
        await state.finish()


@dp.message_handler(commands=['updateINN'])
async def say_pin(message: types.Message, state: FSMContext):
    await message.answer('Для этого введите ваш ИНН')
    await UserState.updatePin.set()


@dp.message_handler(state=UserState.updatePin)
async def update_pin(message: types.Message, state: FSMContext):
    await state.update_data(user_new_pin=message.text)
    data = await state.get_data()
    user_pin = data['user_new_pin']
    if len(user_pin) == 14:
        remake_pin = accaunts.pin_remake_by_id(message.from_user.id, user_pin)
        if remake_pin:
            await message.answer('Вы успешно поменяли свой ИНН)')
            await state.finish()
    else:
        await message.answer('Ввели некорректный ИНН. Попробуйте снова!')
        await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
