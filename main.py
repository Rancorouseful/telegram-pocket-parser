from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import aiohttp
import requests
import os

from config import config
from utils import keyboards, db_connect
from utils.get_page import get

#--- Подключение бота
API_TOKEN = config.TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#--- Функции проверки польователя
async def is_exists(chat_id):
    if db_connect.is_exist(chat_id): 
        return True
    return False

async def send_if_not_exists(chat_id):
    await bot.send_message(chat_id, '⭕️ Relaunch bot */start*')
    return

#--- Обработка команд
@dp.message_handler(commands=['start', 'menu'])
async def send_welcome(message: types.Message):

    chat_id = message.chat.id

    # Добавить пользователя
    db_connect.add_user(chat_id, 'EN')

    await bot.send_message(chat_id, "Welcome to @pocketParserBot!", reply_markup=keyboards.request_keyboard)



#--- Обработка текста

# chat_id (Ожидание ссылки в сообщении)
wait_for_url = []

@dp.message_handler()
async def echo(message: types.Message):

    chat_id = message.chat.id

    if not await is_exists(chat_id): 
        await send_if_not_exists(chat_id)
    if chat_id not in wait_for_url:
        await bot.send_message(chat_id, "I can't recognize the meaning of the message. Repeat your request and leave a message again.")
        return
    
    # Добавить префикс "http://" к введенному URL, если его нет
    user_input = message.text
    if not user_input.startswith(("https://", "http://")):
        user_input = "http://" + user_input

    # Попытаться отправить GET-запрос и проверить статус ответа
    try:
        response = requests.get(user_input)
        if response.status_code == 200:
            await bot.send_message(chat_id, f'Got: {user_input}')
        else:
            await bot.send_message(chat_id, f'Server response, when accessed by {user_input}: {response.status_code}')
            return

    except requests.exceptions.MissingSchema:
        await bot.send_message(chat_id, "Can't identify \"{message.text}\" as a url")
        return
    except requests.exceptions.RequestException as e:
        await bot.send_message(chat_id, f"Can't identify \"{message.text}\" as a working url")
        return
    
    mode = db_connect.get_chosen_mode(chat_id)
    
    if mode == 'get_html':
        file = await get.html(chat_id, user_input)
        if file:
            # Отправляем файл пользователю в Telegram
            with open(file, 'rb') as html_file:
                await bot.send_document(chat_id, document=html_file)
            wait_for_url.remove(chat_id)
        else:
            await bot.send_message(chat_id, f'An error occurred, please, try something else.')
        os.remove(file)
    elif mode == 'get_style':
        links = await get.styles(chat_id, user_input)
        if links:
            # Отправляем список ссылок
            links = "\n•".join(links)
            await bot.send_message(chat_id, f'Вот все ссылки на стили сайта:\n•{links}')
            wait_for_url.remove(chat_id)
        else:
            await bot.send_message(chat_id, f"Couldn't find links to styles")

    

#--- Обработка callback_data 

@dp.callback_query_handler(lambda c: c.data in keyboards.REQUEST_BUTTONS)
async def set_mode(c: types.CallbackQuery):
    chat_id = c.message.chat.id

    if not await is_exists(chat_id):
        await send_if_not_exists(chat_id)
    
    answers = {
        keyboards.REQUEST_BUTTONS[0]: ["OK, send the URL of the site or its page, and I'll send the .txt file with the code.", 'get_html'],
        keyboards.REQUEST_BUTTONS[1]: ["OK, send the URL of the site or its page, and I'll send the .txt file with the code.", 'get_style'],
    }

    await bot.send_message(chat_id, answers[c.data][0])

    db_connect.set_chosen_mode(chat_id, answers[c.data][1])
    wait_for_url.append(chat_id)

#--- Непрерывная работа
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)


