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
cat_btn.add(InlineKeyboardButton(_("Xitoy"), callback_data="catXitoy"))
cat_btn.add(InlineKeyboardButton(_("Turkiya"), callback_data="catTurkiya"))
cat_btn.add(InlineKeyboardButton(_("Yevropa"), callback_data="catYevropa"))
cat_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))


road_btn = InlineKeyboardMarkup(row_width=1)
road_btn.add(InlineKeyboardButton(_("Temir yo'l 🚂"), callback_data="Temir yo'l"))
road_btn.add(InlineKeyboardButton(_("Avto 🚛"), callback_data="Avto"))
road_btn.add(InlineKeyboardButton(_("Avia ✈️"), callback_data="Avia"))
road_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))


async def weight_btns(road_type=False):
    weight_btn = InlineKeyboardMarkup(row_width=1)
    if road_type:
        weight_btn.add(InlineKeyboardButton(_("To'liq konteyner (40HC, 20GP)"), callback_data="To'liq konteyner (40HC, 20GP)"))
    else:
        weight_btn.add(InlineKeyboardButton(_("To'liq fura (90, 120)"), callback_data="To'liq fura (90, 120)"))
    weight_btn.add(InlineKeyboardButton(_("Yeg'ma yuk (Sborniy)"), callback_data="Yeg'ma yuk (Sborniy)"))
    weight_btn.add(InlineKeyboardButton(_("Orqaga 🔙"), callback_data="back"))
    return weight_btn

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

