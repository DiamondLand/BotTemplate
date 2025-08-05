from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from src.elements.keybord.text_on_kb import cancel


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=cancel)]]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
