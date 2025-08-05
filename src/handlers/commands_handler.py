import psutil

from loguru import logger

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink

from src.database.services import get_or_create_user_service, get_users_service
from src.functions.greeting import send_greeting
from src.elements.inline.other_inline import support_button
from src.elements.keybord.kb import cancel_kb
from src.events.states_group import Utils
from src.config.advertisement import support_link

router = Router()


# --- Основная панель --- #
@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await message.answer(
            text="🔎✨",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

    try:
        await get_or_create_user_service(user_id=message.from_user.id)
    except Exception as _ex:
        logger.debug(f"Не удалось проверить аккаунт: {_ex}")

    await message.answer(
        text=f"{send_greeting(username=message.from_user.first_name)}"
    )


# --- Информационнная панель --- #
@router.message(Command("info"))
async def info_cmd(message: Message, state: FSMContext):
    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await message.answer(
            text="🔎✨",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

    botname = message.bot.config['SETTINGS']['name']
    message_text = (
        f"<b>СПРАВКА {hlink(botname, support_link)} v{message.bot.config['SETTINGS']['version']}:</b>"
    )

    await message.answer(
        text=message_text,
        reply_markup=support_button().as_markup()
    )


# --- Отправка статистики --- #
@router.message(Command("statistic", "bin"))
async def statistic_cmd(message: Message, state: FSMContext):
    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await message.answer(
            text="🔎✨",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
    
    if int(message.chat.id) in map(int, message.bot.ADMIN_CHATS):
        users_data = await get_users_service()
        if users_data:
            users_count = f"<b>Пользователей:</b> <code>{len(users_data)}</code>"
        else:
            users_count = "<b>Информации о пользователях нет</b>!"

        await message.answer(
            text=f"<b>СТАТИСТИКА:</b>\
                \n\n{users_count}\
                \n\n<b>CPU:</b> <code>{psutil.cpu_percent(interval=1)}</code> | <b>RAM:</b> <code>{psutil.virtual_memory().percent}</code>%\
                \n<b>Использовано дискового пространства:</b> <code>{psutil.disk_usage('/').percent}</code>%"
        )


# --- Перейти в рассылку -> Написать текст --- #
@router.message(Command("mailing", "bin2"))
async def mailing_cmd(message: Message, state: FSMContext):
    # Если стадия существует, выходим из неё
    if await state.get_state() is not None:
        await message.answer(
            text="🔎✨",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

    if int(message.chat.id) in map(int, message.bot.ADMIN_CHATS):
        await message.answer(
            text="💥 Введите <u>текст</u> или прикрепите <u>медиаконтент</u>, который будет отправлен всем пользователям:", 
            reply_markup=cancel_kb()
        )
        await state.set_state(Utils.mailing)
