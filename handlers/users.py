from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.db import Database

router = Router()

db = Database("performers.sql")


@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
            await message.answer("Добро пожаловать в семью!")
        else:
            await message.answer("Ты уже в семье!")


@router.message(Command("users"))
async def cmd_users(message: Message):
    users = db.get_users()
    spisok = "Работники:"
    i = 0
    for r in users:
        spisok += f"\n id = {r[0]}, tag_name = @{r[1]}, имя = {r[2]}, статус : "
        if r[3] == 1:
            spisok += "активен"
        else:
            spisok += "не активен"
        i += 1
    await message.answer(spisok)


@router.message(Command("orders"))
async def cmd_users(message: Message):
    orders = db.get_orders(message.from_user.id)
    text = (f"Исполнитель: {message.from_user.id} \n"
            f"Номера заказов: ")
    for r in orders:
        text += f"\n{r[0]}"
    await message.answer(text)
