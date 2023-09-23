from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LANGUAGE_BUTTONS = ['ENG 🇬🇧', 'RUS 🇷🇺']

btn_eng = InlineKeyboardButton(LANGUAGE_BUTTONS[0], callback_data=LANGUAGE_BUTTONS[0])
btn_rus = InlineKeyboardButton(LANGUAGE_BUTTONS[1], callback_data=LANGUAGE_BUTTONS[1])
language_keyboard = InlineKeyboardMarkup(row_width=2).add(btn_eng, btn_rus)


