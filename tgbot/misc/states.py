from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    get_lang = State()
    get_cat = State()


class UserPrice(StatesGroup):
    get_name = State()
    get_phone = State()
    get_cat = State()


class UserCargo(StatesGroup):
    get_id = State()
    get_choice = State()
    get_cargo = State()


class UserSettings(StatesGroup):
    get_lang = State()
