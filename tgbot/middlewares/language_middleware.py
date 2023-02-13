from typing import Tuple, Any, Optional
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from tgbot.config import I18N_DOMAIN, LOCALES_DIR
from tgbot.models.models import DBCommands

db = DBCommands()


async def get_lang(user_id):
    user = await db.get_user(user_id)
    if user:
        return str(user.lang)


class ACLMiddleware(I18nMiddleware):

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale
