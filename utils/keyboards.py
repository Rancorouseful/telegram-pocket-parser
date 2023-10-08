from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

REQUEST_BUTTONS = ['Get HTML', 'Get Stylesheet']

get_html = InlineKeyboardButton(REQUEST_BUTTONS[0], callback_data=REQUEST_BUTTONS[0])
get_style = InlineKeyboardButton(REQUEST_BUTTONS[1], callback_data=REQUEST_BUTTONS[1])
request_keyboard = InlineKeyboardMarkup(row_width=2).add(get_html, get_style)
