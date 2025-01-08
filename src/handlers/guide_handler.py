import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.logs.config import configure_logging
from src.messages.guide_messages import GUIDE_MESSAGE


logger = logging.getLogger(__name__)
configure_logging()

router = Router()


@router.message(Command("guide"))
async def command_guide_handler(message: Message):
    """
    Функция для получения инструкции по использованию аккаунта

    :param Message message: Сообщение от пользователя
    :return: None
    """
    logger.info("New guide request from user: %r", message.from_user.id)
    await message.answer(text=GUIDE_MESSAGE, parse_mode="html")
