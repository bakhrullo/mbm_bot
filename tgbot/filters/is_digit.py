import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsDigitFilter(BoundFilter):

    def __init__(self, is_digit: typing.Optional[bool] = None):
        self.is_digit = is_digit

    async def check(self, call: types.CallbackQuery):
        if call.data.isdigit() and self.is_digit:
            return True
        return False
