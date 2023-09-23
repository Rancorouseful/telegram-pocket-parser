from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import gettext

from config import config
from utils import keyboards, db_connect

#--- Подключение бота
API_TOKEN = config.TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#--- Настройка языков
#TODO


#--- Обработка команд
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    chat_id = message.chat.id

    if db_connect.is_exist(chat_id):  
        #TODO
        pass

    await bot.send_message(chat_id, "Выбери язык бота / Choose bot language", reply_markup=keyboards.language_keyboard)

#--- Обработка callback_data 
@dp.callback_query_handler(lambda c: c.data in keyboards.LANGUAGE_BUTTONS)
async def return_to_styles(c: types.CallbackQuery):

    chat_id = c.message.chat.id

    # Добавить пользователя
    db_connect.add_user(chat_id, c.data.split(' ')[0])


#--- Непрерывная работа
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)


