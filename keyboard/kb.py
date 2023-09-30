from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Принять")
    kb.button(text="Отказаться")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def order_status_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Выполнено")
    kb.button(text="Отказался")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)