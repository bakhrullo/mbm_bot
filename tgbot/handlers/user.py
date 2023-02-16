import asyncio
import types

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import menu_btns, back_btn, cat_btn, lang_btns, choice_btn, cargo_btns, road_btn, \
    weight_btns
from tgbot.keyboards.reply import contact_btn, remove_btn
from tgbot.misc.add_or_update import add_or_update
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import UserState, UserPrice, UserSettings, UserCargo
from tgbot.models import models

_ = i18ns.gettext
__ = i18ns.lazy_gettext

db = models.DBCommands()


async def get_doc(m: Message, scheduler):
    config = m.bot.get("config")
    if m.from_user.id in config.tg_bot.admin_ids:
        doc = str(m.from_user.id)
        await m.document.download(destination_file=f"{doc}.xlsx")
        await m.answer("⏳")
        await m.answer("Iltimos biroz kutib turing")
        await add_or_update(doc, m)
        try:
            scheduler.remove_job("job")
        except:
            pass
    else:
        pass


async def user_start(m: Message):
    chat_id = m.from_user.id
    user = await db.get_user(chat_id)
    if user:
        await m.answer(_("Kerakli bo'limni tanlang! 👇"), reply_markup=await menu_btns())
        await UserState.get_cat.set()
    else:
        await m.reply(_("Assalomualaykum! 👋\nBotimizga xushkelibsiz kerakli tilni tanlang"),
                      reply_markup=await lang_btns(False))
        await UserState.get_lang.set()


async def get_lang(c: CallbackQuery):
    lang = c.data.replace("lang", "")
    await db.add_new_user(lang)
    await c.message.edit_text(_("Kerakli bo'limni tanlang! 👇", locale=lang), reply_markup=await menu_btns(lang))
    await UserState.get_cat.set()


async def price(c: CallbackQuery):
    await c.message.edit_text(_("Iltimos ismingizni kiriting 👤"), reply_markup=back_btn)
    await UserPrice.get_name.set()


async def settings(c: CallbackQuery):
    await c.message.edit_text(_("Tilni o\'zgartirish 🔄"), reply_markup=await lang_btns(True))
    await UserSettings.get_lang.set()


async def cargo(c: CallbackQuery):
    await c.message.edit_text(_("Iltimos ID raqamingizni kiriting 🆔"), reply_markup=back_btn)
    await UserCargo.get_id.set()


async def get_id(m: Message, state: FSMContext):
    res = await db.get_cargos(m.text)
    if res:
        await state.update_data(id=m.text)
        await m.answer(_("👤 Shaxsiy kabinetga xush kelibsiz"), reply_markup=choice_btn)
        await UserCargo.get_choice.set()
    else:
        await m.answer(_("❌ Xato id kiritildi. Ilitimos qayta tekshiib kiriting"))


async def get_choice(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    res = await db.get_cargos(data['id'])
    await c.message.edit_text(_("Yuklaringizdan birini tanlang! 👇"), reply_markup=await cargo_btns(res))
    await UserCargo.get_cargo.set()


async def get_cargo(c: CallbackQuery):
    res = await db.get_cargo(int(c.data))
    await c.message.edit_text(_("🤵‍♂️ Hurmatli {user_name}\n"
                                "📦 Siz {container_type} {container_number} buyurtma bergansiz.\n"
                                "📅 Yuklash sanasi: {load_date}\n"
                                "📥 Yuklash Manzili: {load_address}\n"
                                "📅 Yuborish sanasi: {send_date}\n"
                                "📬 Dislokatsiya: {dislocation}\n"
                                "📤 Yetkazish manzili: {delivery_address}\n"
                                "↗️ Buyurtma yo'nalishi: {burning_address}\n"
                                "📅 Kelish sanasi: {arrival_date}").format(
        user_name=res.user_name,
        container_type=res.container_type,
        container_number=res.cargo_number,
        load_date=res.load_date,
        load_address=res.load_address,
        send_date=res.send_date,
        dislocation=res.dislocation,
        delivery_address=res.delivery_address,
        burning_address=res.burning_address,
        arrival_date=res.arrival_date),
                          reply_markup=back_btn)


async def change_lang(c: CallbackQuery):
    lang = c.data.replace("lang", "")
    await db.set_language(language=lang)
    await c.message.edit_text(_("Tili o\'zgartirildi", locale=lang))
    await c.message.answer(_("Kerakli bo'limni tanlang! 👇", locale=lang), reply_markup=await menu_btns(lang))
    await UserState.get_cat.set()


async def get_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer(_("Iltimos telefon raqamingizin kiriting 📲"), reply_markup=contact_btn)
    await UserPrice.get_phone.set()


async def get_phone(m: Message, state: FSMContext):
    await state.update_data(phone=m.contact.phone_number)
    await m.answer(_("Yukingiz qaysi davlatda joylashgan?"), reply_markup=remove_btn)
    await m.answer(_("Kerakli bo\'lgan yo\'nalishni tanlang 👇"), reply_markup=cat_btn)
    await UserPrice.get_cat.set()


async def get_cat(c: CallbackQuery, state: FSMContext):
    await state.update_data(cat=c.data.replace('cat', ''))
    await c.message.edit_text(_("Transport turini tanlang 👇"), reply_markup=road_btn)
    await UserPrice.get_road.set()


async def get_road(c: CallbackQuery, state: FSMContext):
    await state.update_data(road=c.data)
    if c.data == "Avia":
        await UserPrice.get_weight_a.set()
        return await c.message.edit_text(_("Yukingiz hajmi kiriting ↔️"), reply_markup=back_btn)
    elif c.data == "Temir yo'l":
        btn = await weight_btns(True)
    else:
        btn = await weight_btns()
    await c.message.edit_text(_("Yukingiz hajmini tanlang 👇"), reply_markup=btn)
    await UserPrice.get_weight_type.set()


async def get_weight_a(m: Message, state: FSMContext):
    await state.update_data(weight_a=m.text)
    await m.answer(_("Yukingiz og\'irligini kiriting "), reply_markup=back_btn)
    await UserPrice.get_weight_cargo_a.set()


async def get_weight_cargo_a(m: Message, state: FSMContext):
    config = m.bot.get("config")
    data = await state.get_data()
    await m.answer(_("Raxmat, so'rovingiz qabul qilindi!\n"
                     "Siz bilan tez orada agentimiz bog'lanadi. 👨‍💻\n"
                     "Tanlovingiz uchun raxmat. 😃"))
    for i in config.tg_bot.group_ids:
        await m.bot.send_message(chat_id=i, text=f"👨 Ismi: {data['name']}\n"
                                                 f"📞 Telefon raqam: {data['phone']}\n"
                                                 f"🔄 Yuk joylashgan davlat: {data['cat']}\n"
                                                 f"🚚 Transport turi: {data['road']}\n"
                                                 f"📦 Yukning hajimi: {data['weight_a']}\n"
                                                 f"⚖️ Yuk og\'irligi: {m.text}\n")
        await asyncio.sleep(.05)
    await state.reset_state()
    await m.answer(_("Kerakli bo'limni tanlang! 👇"), reply_markup=await menu_btns())
    await UserState.get_cat.set()


async def get_weight_type(c: CallbackQuery, state: FSMContext):
    print('fe')
    await state.update_data(weight_type=c.data)
    if c.data in ["To'liq fura (90, 120)", "To'liq konteyner (40HC, 20GP)"]:
        await c.message.edit_text(_("Yukingiz qaysi shaharda joylashgan? 🏙"), reply_markup=back_btn)
        await UserPrice.get_county.set()
    else:
        await c.message.edit_text(_("Yuk hajmini kiriting 📦"), reply_markup=back_btn)
        await UserPrice.get_weight.set()


async def get_country(m: Message, state: FSMContext):
    await state.update_data(county=m.text, type="to")
    await m.answer(_("Yukingiz qachon tayyor bo'ladi? 📆"), reply_markup=back_btn)
    await UserPrice.get_date.set()


async def get_weight(m: Message, state: FSMContext):
    await state.update_data(weight=m.text)
    await m.answer(_("Yuk og'irligini kiriting"), reply_markup=back_btn)
    await UserPrice.get_weight_cargo.set()


async def get_weight_cargo(m: Message, state: FSMContext):
    await state.update_data(weight_cargo=m.text)
    await m.answer(_("Yukingiz yuklanishga tayyormi?"), reply_markup=back_btn)
    await UserPrice.get_confirm.set()


async def get_confirm(m: Message, state: FSMContext):
    await state.update_data(confirm=m.text, type="sb")
    await m.answer(_("Iltimos yuklanish sanasini kiriting"), reply_markup=back_btn)
    await UserPrice.get_date.set()


async def get_date(m: Message, state: FSMContext):
    config = m.bot.get("config")
    data = await state.get_data()
    await m.answer(_("Raxmat, so'rovingiz qabul qilindi!\n"
                     "Siz bilan tez orada agentimiz bog'lanadi. 👨‍💻\n"
                     "Tanlovingiz uchun raxmat. 😃"))
    for i in config.tg_bot.group_ids:
        if data["type"] == "to":
            await m.bot.send_message(chat_id=i, text=f"👨 Ismi: {data['name']}\n"
                                                     f"📞 Telefon raqam: {data['phone']}\n"
                                                     f"🔄 Yuk joylashgan davlat: {data['cat']}\n"
                                                     f"🚚 Transport turi: {data['road']}\n"
                                                     f"📦 Yukning hajimi: {data['weight_type']}\n"
                                                     f"🏙 Yuk joylashgan shahar: {data['county']}\n"
                                                     f"📆 Yuk tayyor bo\'lish sanasi: {m.text}")
        if data["type"] == "sb":
            await m.bot.send_message(chat_id=i, text=f"👨 Ismi: {data['name']}\n"
                                                     f"📞 Telefon raqam: {data['phone']}\n"
                                                     f"🔄 Yuk joylashgan davlat: {data['cat']}\n"
                                                     f"🚚 Transport turi: {data['road']}\n"
                                                     f"📦 Yukning hajimi turi: {data['weight_type']}\n"
                                                     f"↔️ Yukninig hajimi: {data['weight']}\n"
                                                     f"⚖️ Yuk og\'irligi: {data['weight_cargo']}\n"
                                                     f"✅ Yuk holati: {data['confirm']}\n"
                                                     f"📆 Yuk tayyor bo\'lish sanasi: {m.text}")
        await asyncio.sleep(.05)
    await state.reset_state()
    await m.answer(_("Kerakli bo'limni tanlang! 👇"), reply_markup=await menu_btns())
    await UserState.get_cat.set()


async def back(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(_("Kerakli bo'limni tanlang! 👇"), reply_markup=await menu_btns())
    await state.reset_state()
    await UserState.get_cat.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(get_lang, state=UserState.get_lang)
    dp.register_callback_query_handler(price, Text(equals="price"), state=UserState.get_cat)
    dp.register_callback_query_handler(settings, Text(equals="settings"), state=UserState.get_cat)
    dp.register_callback_query_handler(cargo, Text(equals="cargo"), state=UserState.get_cat)
    dp.register_callback_query_handler(change_lang, Text(startswith="lang"), state=UserSettings.get_lang)
    dp.register_message_handler(get_name, state=UserPrice.get_name)
    dp.register_message_handler(get_id, state=UserCargo.get_id)
    dp.register_message_handler(get_phone, content_types=types.ContentType.CONTACT, state=UserPrice.get_phone)
    dp.register_callback_query_handler(get_cat, Text(startswith="cat"), state=UserPrice.get_cat)
    dp.register_callback_query_handler(get_choice, Text(startswith="cargo"), state=UserCargo.get_choice)
    dp.register_callback_query_handler(get_cargo, BackFilter(), state=UserCargo.get_cargo)
    dp.register_callback_query_handler(get_road, BackFilter(), state=UserPrice.get_road)
    dp.register_message_handler(get_weight_a, state=UserPrice.get_weight_a)
    dp.register_message_handler(get_weight_cargo_a, state=UserPrice.get_weight_cargo_a)
    dp.register_callback_query_handler(get_weight_type, BackFilter(), state=UserPrice.get_weight_type)
    dp.register_message_handler(get_country, state=UserPrice.get_county)
    dp.register_message_handler(get_weight, state=UserPrice.get_weight)
    dp.register_message_handler(get_weight_cargo, state=UserPrice.get_weight_cargo)
    dp.register_message_handler(get_confirm, state=UserPrice.get_confirm)
    dp.register_message_handler(get_date, state=UserPrice.get_date)
    dp.register_callback_query_handler(back, state="*")
    dp.register_message_handler(get_doc, content_types=types.ContentType.DOCUMENT, state="*")
