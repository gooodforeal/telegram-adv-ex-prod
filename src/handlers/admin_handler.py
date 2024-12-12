import logging
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from src.config import settings
from src.logs.config import configure_logging
from src.keyboards.admin_kb import get_admin_kb
from src.repositories.users_repository import UsersRepository

logger = logging.getLogger(__name__)
configure_logging()

router = Router()


@router.message(F.text == "📋 Список пользователей")
async def command_admin(message: Message, bot: Bot):
    if message.from_user.id == settings.ADMIN_ID:
        users_list = await UsersRepository.find_all()
        formated_list = [f"ID: {user.id}\nTG_ID: {user.tg_id}\nДата регистрации: {user.created_at}"
                         f"\nПоследняя выдача: {user.last_time_given}\nРеферал: {user.is_reffed}" for user in
                         users_list]
        for user in formated_list:
            await message.answer(
                text=user
            )
    else:
        await message.answer(
            text=f"⛔️ Вы не являетесь администратором!"
        )


@router.message(Command("admin"))
async def command_admin(message: Message, bot: Bot):
    logger.info("New admin panel request from user: %r", message.from_user.id)
    if message.from_user.id == settings.ADMIN_ID:
        await message.answer(
            text=f"Вы админ!",
            reply_markup=get_admin_kb()
        )
    else:
        await message.answer(
            text=f"⛔️ Вы не являетесь администратором!"
        )
