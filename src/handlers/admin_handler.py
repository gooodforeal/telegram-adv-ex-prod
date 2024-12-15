import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from src.config import settings
from src.logs.config import configure_logging
from src.keyboards.admin_kb import get_admin_kb
from src.repositories.users_repository import UsersRepository
from src.repositories.accounts_repository import AccountsRepository

logger = logging.getLogger(__name__)
configure_logging()

router = Router()


@router.message(F.text.startswith('add:'))
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        try:
            account_dto = [
                {
                    "username": acc.split(":")[0],
                    "password": acc.split(":")[1],
                    "games": acc.split(":")[2]
                }
                for acc in message.text.split("\n")[1::]
            ]
            await AccountsRepository.add_many(data=account_dto)
            await message.answer(
                text=f"✅ Аккаунты успешно добавлены в систему!"
            )

        except Exception as ex:
            logger.error("Invalid data format %s", ex)
            await message.answer(
                text=f"⛔️ Неправильный формат ввода данных!"
            )
    else:
        await message.answer(
            text=f"⛔️ Вы не являетесь администратором!"
        )


@router.message(F.text == "➕ Добавить аккаунт")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        await message.answer(
            text=f"Отправьте аккаунты которые необходимо добавить в формате:"
                 f"\n\nadd:\nlogin1:password1:games1\nlogin2:password:games2!"
        )
    else:
        await message.answer(
            text=f"⛔️ Вы не являетесь администратором!"
        )


@router.message(F.text == "📋 Список аккаунтов")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        accounts_list = await AccountsRepository.find_all()
        formated_list = [
            f"ID: {acc.id}\n"
            f"👤 Логин: {acc.username}\n"
            f"🔐 Пароль: {acc.password}\n"
            f"🎮 Игры: {acc.games}"
            for acc in accounts_list
        ]
        if len(formated_list):
            for acc in formated_list:
                await message.answer(
                    text=acc
                )
        else:
            await message.answer(
                text="📋 Список аккаунтов пуст!"
            )
    else:
        await message.answer(
            text=f"⛔️ Вы не являетесь администратором!"
        )


@router.message(F.text == "📋 Список пользователей")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        users_list = await UsersRepository.find_all()
        formated_list = [
            f"📌 ID: {user.id}\n"
            f"📌 TG_ID: {user.tg_id}\n"
            f"⏰ Дата регистрации: {user.created_at}\n"
            f"📲 Последняя выдача: {user.last_time_given}\n"
            f"👤 Реферал: {user.is_reffed}"
            for user in users_list
        ]
        if len(formated_list):
            for user in formated_list:
                await message.answer(
                    text=user
                )
        else:
            await message.answer(
                text="📋 Список пользователей пуст!"
            )
    else:
        await message.answer(
            text=f"⛔️ Вы не являетесь администратором!"
        )


@router.message(Command("admin"))
async def command_admin(message: Message):
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
