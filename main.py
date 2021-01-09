import db_users as db
from settings import API_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    db.check_and_add_user(message)
    text = f"Привет {message.from_user.first_name}, здесь ты сможешь добавлять слова" \
           " и их перевод для изучения.\n" \
           "Для получения списка команд введи:\n/help"
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands=['help'])
async def commands_list(message: types.Message):
    text = "А вот и список команд:\n" \
           "/add_words - добавить слово и перевод\n" \
           "/try_to_translate - попробовать перевести " \
           "случайное слово"
    await message.answer(text)


@dp.message_handler(commands=['add_words'])
async def add_words(message: types.Message):
    await message.answer("Введи любое слово:")
    await message.answer(message.text)


def return_message(message):
    return message


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
