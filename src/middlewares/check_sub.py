import logging
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message

from src.config import settings
from src.logs.config import configure_logging
from src.messages.startup_messages import not_sub_message
from src.keyboards.sub_kb import get_sub_kb


logger = logging.getLogger(__name__)
configure_logging()


class CheckSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger.info("Check subscription start! User: %r", event.from_user.id)
        chat_member = await event.bot.get_chat_member(settings.CHANNEL_ID, event.from_user.id)
        if chat_member.status == "left":
            await event.answer(text=not_sub_message, reply_markup=get_sub_kb())
        else:
            return await handler(event, data)
