from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    get_lang = State()
    get_cat = State()


class UserPrice(StatesGroup):
    get_name = State()
    get_phone = State()
    get_cat = State()
    get_road = State()
    get_weight_type = State()
    get_weight = State()
    get_weight_cargo = State()
    get_confirm = State()
    get_county = State()
    get_date = State()
    get_weight_a = State()
    get_weight_cargo_a = State()


class UserCargo(StatesGroup):
    get_id = State()
    get_choice = State()
    get_cargo = State()


class UserSettings(StatesGroup):
    get_lang = State()
