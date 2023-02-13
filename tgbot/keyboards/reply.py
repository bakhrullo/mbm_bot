from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext

contact_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(_("Kontaktni yuborish 📱"), request_contact=True))

remove_btn = ReplyKeyboardRemove()
