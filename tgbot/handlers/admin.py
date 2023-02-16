# from aiogram import Dispatcher, types
# from aiogram.types import Message, InputFile
#
# from tgbot.misc.add_or_update import add_or_update
#
#
# async def admin_start(m: Message):
#     await m.reply("Salom, admin! 👋. Excelni manabu korinishda yuboring")
#     await m.bot.send_document(m.from_user.id, document=InputFile("example.xlsx"))
#
#
# async def get_doc(m: Message, scheduler):
#     doc = str(m.from_user.id)
#     await m.document.download(destination_file=f"{doc}.xlsx")
#     await m.answer("⏳")
#     await m.answer("Iltimos biroz kutib turing")
#     await add_or_update(doc, m)
#     try:
#         scheduler.remove_job("job")
#     except:
#         pass
#
# def register_admin(dp: Dispatcher):
#     dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
#     dp.register_message_handler(get_doc, content_types=types.ContentType.DOCUMENT, state="*", is_admin=True)
