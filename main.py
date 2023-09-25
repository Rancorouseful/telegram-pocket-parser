from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Подключение языков
from language import ru, en

from config import config
from utils import keyboards, db_connect
from utils.get_page import get

#--- Подключение бота
API_TOKEN = config.TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#--- Локализация текста
async def localize(keytext, lang):
    if lang=='ENG': return en.EN[keytext]
    else: return ru.RU[keytext]

#--- Обработка команд
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    chat_id = message.chat.id

    if db_connect.is_exist(chat_id): 
        language = db_connect.get_language(chat_id)
        await bot.send_message(chat_id, await localize('Бот уже запущен', language))
        return

    await bot.send_message(chat_id, "Выбери язык бота / Choose bot language", reply_markup=keyboards.language_keyboard)

#--- Обработка callback_data 
@dp.callback_query_handler(lambda c: c.data in keyboards.LANGUAGE_BUTTONS)
async def return_to_styles(c: types.CallbackQuery):

    chat_id = c.message.chat.id
    language = c.data.split(' ')[0]

    if db_connect.is_exist(chat_id):  
        # Обновить язык
        db_connect.set_language(chat_id, language)
    else:
        # Добавить пользователя
        db_connect.add_user(chat_id, language)

    await bot.send_message(chat_id, await localize('Язык выбран', language), reply_markup=keyboards.content_keyboard)

@dp.callback_query_handler(lambda c: c.data in keyboards.GET_CONTENT)
async def return_to_styles(c: types.CallbackQuery):

    chat_id = c.message.chat.id
    page = get.page('https://beatmaker.site/')
    tag = 'a'

    response = get.tag(page, tag)

    await bot.send_message(chat_id, f'Вот все <a> теги на сайте:\n\n{response}')



#--- Непрерывная работа
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)


