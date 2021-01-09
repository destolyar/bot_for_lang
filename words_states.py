from aiogram.dispatcher.filters.state import State, StatesGroup

class Words(StatesGroup):
    word_on_eng = State()
    word_on_ru = State()