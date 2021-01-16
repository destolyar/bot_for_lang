from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_help = KeyboardButton('/help')

help_call_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_help)

add_words_button = KeyboardButton('/add_words')
translate_button = KeyboardButton('/try_to_translate')
help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(add_words_button, translate_button)