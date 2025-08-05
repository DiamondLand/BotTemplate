import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from tortoise import Tortoise
from typing import Literal
from loguru import logger

from src.config.db import TORTOISE_ORM
from src.config.cfg import cfg, ADMIN_CHATS
from src.middleware.throttling import ThrottlingMiddleware
from src.events import error_handler, states_group
from src.handlers import commands_handler
from src.handlers.utils import mailing

bot = Bot(
    token=cfg["SETTINGS"]["testing_token"], 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
bot.config = cfg
bot.ADMIN_CHATS = ADMIN_CHATS

dp = Dispatcher()

MODE: Literal["DEV", "PROD"] = "DEV"
if MODE == "DEV":
    TOKEN = cfg["SETTINGS"]["testing_token"]
else:
    TOKEN = cfg["SETTINGS"]["token"]

bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
bot.config = cfg
bot.permanent_ids = ADMIN_CHATS

dp = Dispatcher()


async def setup_database():
    logger.info("Connecting to DB...")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    logger.success("DB connected")


async def shutdown():
    logger.info("Shutting down...")
    await Tortoise.close_connections()
    await bot.session.close()
    logger.success("Shutdown complete")


# --- Подгрузка модулей ТГ бота --- #
async def loader():
    logger.info("Loading modules...")

    dp.include_routers(
        error_handler.router,
        states_group.router,
        commands_handler.router,
        mailing.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await setup_database() 
    logger.success("Successfully launched")
    await dp.start_polling(bot)


# Регистрация промежуточного ПО
dp.message.middleware(ThrottlingMiddleware(limit=1, period=0.6))


def main():
    try:
        asyncio.run(loader())
    except:
        asyncio.run(shutdown())
