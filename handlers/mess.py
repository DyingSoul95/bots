from aiogram import Router, Bot, exceptions, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboard.kb import get_yes_no_kb, order_status_kb
from database.db import Database

router = Router()
db = Database("performers.sql")


@router.message(Command("send"))
async def cmd_send(message: Message, bot: Bot):
    if message.chat.type == "private" and message.from_user.id == 803591559:
        text = message.text.split("\n")
        mess = f"Номер заказа : {text[2]} \nЗаказ: "
        for r in text[3:]:
            mess += f"\n{r}"
        try:
            await bot.send_message(text[1], mess, reply_markup=get_yes_no_kb())
        except exceptions.TelegramBadRequest:
            await message.answer("Сообщение отправить не удалось!")
        except exceptions.TelegramForbiddenError:
            db.set_active(text[1], 0)
            await message.answer("Пользователь заблокировал бота!")
        else:
            db.set_order(text[1], text[2])
            db.set_active(text[1], 1)
            await message.answer("Сообщение отправлено!")


@router.message(F.text.lower() == "принять")
async def answer_yes(message: Message, bot: Bot):
    order_number = db.get_order(message.from_user.id)
    await bot.send_message(-4092747951, f"{message.from_user.full_name} принял заказ: {order_number[0][0]}")
    await message.answer("Это здорово!", reply_markup=order_status_kb())


@router.message(F.text.lower() == "отказаться")
async def answer_no(message: Message, bot: Bot):
    order_number = db.get_order(message.from_user.id)
    await bot.send_message(803591559, f"{message.from_user.full_name} отказался от заказа {order_number[0][0]}")
    await message.answer("Жаль!", reply_markup=ReplyKeyboardRemove())


class FSMFillForm(StatesGroup):
    fill_amount_of_work = State()
    fill_amount_of_materials = State()
    fill_guarantee_period = State()
    fill_rejection_reason = State()


@router.message(F.text.lower() == "выполнено", StateFilter(default_state))
async def process_fillform_done_cmd(message: Message, state: FSMContext):
    await message.answer("Укажите сумму работ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFillForm.fill_amount_of_work)


@router.message(F.text, StateFilter(FSMFillForm.fill_amount_of_work))
async def process_work_sent(message: Message, state: FSMContext):
    await state.update_data(amount_of_work=message.text)
    await message.answer(text="Укажите сумму материала")
    await state.set_state(FSMFillForm.fill_amount_of_materials)


@router.message(F.text, StateFilter(FSMFillForm.fill_amount_of_materials))
async def process_materials_sent(message: Message, state: FSMContext):
    await state.update_data(amount_of_materials=message.text)
    await message.answer(text="Укажите срок гарантии в днях")
    await state.set_state(FSMFillForm.fill_guarantee_period)


@router.message(F.text, StateFilter(FSMFillForm.fill_guarantee_period))
async def process_guarantee_sent(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(guarantee_period=message.text)
    user_data = await state.get_data()
    order_number = db.get_order(message.from_user.id)
    await bot.send_message(-4092747951,
                           f"Выполнен заказ {order_number[0][0]} {user_data['amount_of_work']}, {user_data['amount_of_materials']}, {user_data['guarantee_period']}")
    await state.clear()


@router.message(F.text.lower() == "отказался", StateFilter(default_state))
async def process_fillform_refusal_cmd(message: Message, state: FSMContext):
    await message.answer("Укажите причину отказа", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFillForm.fill_rejection_reason)


@router.message(F.text, StateFilter(FSMFillForm.fill_rejection_reason))
async def process_guarantee_sent(message: Message, state: FSMContext, bot: Bot):
    order_number = db.get_order(message.from_user.id)
    await bot.send_message(-4092747951,
                           f"{message.from_user.full_name} отказался от заказа {order_number[0][0]} "
                           f"\nПричина: {message.text}")
    await state.clear()


