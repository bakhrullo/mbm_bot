from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext


async def lang_btns(back):
    lang_btn = InlineKeyboardMarkup(row_with=1).add(InlineKeyboardButton("uz 🇺🇿", callback_data="languz"),
                                                    InlineKeyboardButton("ru 🇷🇺", callback_data="langru"),
                                                    InlineKeyboardButton("en 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="langen"))
    if back:
        lang_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))
    return lang_btn


async def menu_btns(locale=False):
    menu_btn = InlineKeyboardMarkup(row_with=1)
    if locale:
        menu_btn.add(InlineKeyboardButton(_("💸 Narxni hisoblatish", locale=locale), callback_data="price"))
        menu_btn.add(InlineKeyboardButton(_("📦 Yuk haqida ma'lumot olish", locale=locale), callback_data="cargo"))
        menu_btn.add(InlineKeyboardButton(_("🛠 Sozlamalar", locale=locale), callback_data="settings"))
    else:
        menu_btn.add(InlineKeyboardButton(_("💸 Narxni hisoblatish"), callback_data="price"))
        menu_btn.add(InlineKeyboardButton(_("📦 Yuk haqida ma'lumot olish"), callback_data="cargo"))
        menu_btn.add(InlineKeyboardButton(_("🛠 Sozlamalar"), callback_data="settings"))
    return menu_btn

cat_btn = InlineKeyboardMarkup(row_width=1)

cat_btn.add(InlineKeyboardButton(_("Pekin - Toshkent"), callback_data="catPekin - Toshkent"))
cat_btn.add(InlineKeyboardButton(_("Toshkent - Pekin"), callback_data="catToshkent - Pekin"))
cat_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))


choice_btn = InlineKeyboardMarkup(row_width=1)

choice_btn.add(InlineKeyboardButton(_("📦 Yuk haqida ma'lumot olish"), callback_data="cargo_info"))
choice_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))


async def cargo_btns(res):
    cargo_btn = InlineKeyboardMarkup(row_width=1)
    for i in res:
        cargo_btn.add(InlineKeyboardButton(f"{i.container_type} {i.cargo_number}", callback_data=i.id))
    cargo_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))
    return cargo_btn

back_btn = InlineKeyboardMarkup().add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))

