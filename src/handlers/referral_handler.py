import logging

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from src.logs.config import configure_logging
from src.messages.refferal_messages import REF_MESSAGE


logger = logging.getLogger(__name__)
configure_logging()

router = Router()


@router.message(Command("ref"))
async def command_ref_handler(message: Message, bot: Bot):
    """
    Функция для получения реферальной ссылки пользователя

    :param Message message: Сообщение от пользователя
    :param Bot bot: Экземпляр бота
    :return: None
    """
    logger.info("New referral link request from user: %r", message.from_user.id)
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    await message.answer(text=REF_MESSAGE.format(link))
