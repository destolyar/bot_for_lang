import db_users as db
from settings import API_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import keyboard as kb

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Answers(StatesGroup):
    word = State()
    translate = State()
    w1 = State()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    db.check_and_add_user(message)
    text = f"Привет {message.from_user.first_name}, здесь ты сможешь добавлять слова" \
           " и их перевод для изучения.\n" \
           "Для получения списка команд введи либо нажми:\n/help"
    await bot.send_message(message.chat.id, text, reply_markup=kb.help_call_kb)


@dp.message_handler(commands=['help'])
async def commands_list(message: types.Message):
    text = "А вот и список команд:\n" \
           "/add_words - добавить слово и перевод\n" \
           "/try_to_translate - попробовать перевести " \
           "случайное слово"
    await message.answer(text, reply_markup=kb.help_kb)


@dp.message_handler(commands=['add_words'])
async def add_words(message: types.Message):
    await message.answer("Введи любое слово:")
    await Answers.word.set()


@dp.message_handler(state=Answers.word)
async def word_for_translate(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data({"answer1": answer1})
    await message.answer("Введите перевод")
    await Answers.next()


@dp.message_handler(state=Answers.translate)
async def translate_of_word(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text
    user_id = message.from_user.id

    await message.answer(f"Ваше слово: \n{answer1}\nЕго перевод: \n{answer2}")

    db.add_word_in_bd(answer1, answer2, user_id)
    await state.finish()


@dp.message_handler(commands=['try_to_translate'])
async def try_to_translate(message: types.Message):
    words = db.take_word(message.from_user.id)
    for eng_word in words:
        pass
    await message.answer(f"Попробуй перевести слово {eng_word}")
    await Answers.w1.set()


@dp.message_handler(state=Answers.w1)
async def check_translate(message: types.Message, state: FSMContext):
    answer = message.text
    translate = db.take_word(message.from_user.id)
    for eng_word in translate:
        pass
    translate = translate[f'{eng_word}']
    if answer.lower() == translate:
        await message.answer(f"Да, верно! Слово {eng_word} действительно переводится как {translate}")
    else:
        await message.answer("Нет, попробуй ещё.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
