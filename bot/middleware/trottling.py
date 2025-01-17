from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message


class AdminMessageMiddleware(BaseMiddleware):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        # Если сообщение получено в группе или супергруппе 
        if event.chat.type in ['group', 'supergroup']:
            admins = await self.bot.get_chat_administrators(event.chat.id)
            admin_ids = [admin.user.id for admin in admins]

            # При использовании команды
            if event.from_user.id not in admin_ids:
                return await event.reply(
                    text="Воспользоваться данной командой может только администратор группы! Вас же приглашаем в личный чат с ботом - @HelperKipBot"
                )

        return await handler(event, data)


class AdminCallbackMiddleware(BaseMiddleware):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        if event.message.chat.type in ['group', 'supergroup']:
            admins = await self.bot.get_chat_administrators(event.message.chat.id)
            admin_ids = [admin.user.id for admin in admins]

            if event.from_user.id not in admin_ids:
                return await event.answer(
                    text="Воспользоваться данной функцией может только администратор группы!", 
                    show_alert=True
                )

        return await handler(event, data)
