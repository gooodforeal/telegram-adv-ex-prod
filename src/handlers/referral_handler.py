import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from src.logs.config import configure_logging


logger = logging.getLogger(__name__)
configure_logging()


router = Router()


@router.message(Command("ref"))
async def command_ref(message: Message, bot: Bot):
    logger.info("New referral link request from user: %r", message.from_user.id)
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    await message.answer(
        text=f"Если сможешь привести друга, то получишь еще один аккаунт со случайной топовой игрой!"
             f"\n\n👉 Твоя реферальная ссылка: {link}"
    )