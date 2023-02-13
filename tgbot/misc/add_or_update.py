import openpyxl
from aiogram.types import Message

from tgbot.models import models

db = models.DBCommands()


async def add_or_update(doc, m: Message):
    book = openpyxl.load_workbook(doc + '.xlsx', read_only=True)
    sheet = book.active
    if sheet['A1'].value is None:
        return await m.answer('Xato formatda yuborildi. Iltimos qayta tekshirib yuboring. ❌')
    row_count = len([row for row in sheet if not all([cell.value is None for cell in row])])
    for i in range(2, row_count+1):
        if sheet[f'A{i}'].value is not None:
            await db.add_or_update(cargo_id=str(sheet[f'A{i}'].value), user_name=str(sheet[f'B{i}'].value),
                                   container_type=str(sheet[f'C{i}'].value), cargo_number=str(sheet[f'D{i}'].value),
                                   load_date=sheet[f'E{i}'].value, load_address=str(sheet[f'F{i}'].value),
                                   send_date=sheet[f'G{i}'].value, dislocation=str(sheet[f'H{i}'].value),
                                   delivery_address=str(sheet[f'I{i}'].value), arrival_date=sheet[f'J{i}'].value,
                                   burning_address=str(sheet[f'K{i}'].value), phone=str(sheet[f'L{i}'].value))
        else:
            return await m.answer(f'Faylda A{i} bo\'sh')
    await m.answer('✅')
    return await m.answer('Import muvaffaqiyatli yakunlandi ✅')