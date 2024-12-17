import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from src.config import settings
from src.logs.config import configure_logging
from src.keyboards.admin_kb import get_admin_kb
from src.repositories.users_repository import UsersRepository
from src.repositories.accounts_repository import AccountsRepository
from src.messages.admin_messages import *

logger = logging.getLogger(__name__)
configure_logging()

router = Router()


@router.message(F.text.startswith('del:'))
async def command_admin(message: Message):
    # Удаление аккаунта из базы
    if message.from_user.id == settings.ADMIN_ID:
        try:
            account_dto = {"id": int(message.text.split("\n")[1])}
            await AccountsRepository.delete(filter_by=account_dto)
            await message.answer(text=success_del_acc_message)
        except Exception as ex:
            logger.error("Invalid data format %s", ex)
            await message.answer(text=invalid_data_message)
    else:
        await message.answer(text=not_admin_message)


@router.message(F.text == "❌ Удалить аккаунт")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        await message.answer(text=del_acc_message, parse_mode="html")
    else:
        await message.answer(text=not_admin_message)


@router.message(F.text.startswith('add:'))
async def command_admin(message: Message):
    # Добавление аккаунта в базу
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
            await message.answer(text=success_add_acc_message)
        except Exception as ex:
            logger.error("Invalid data format %s", ex)
            await message.answer(text=invalid_data_message)
    else:
        await message.answer(text=not_admin_message)


@router.message(F.text == "✅ Добавить аккаунт")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        await message.answer(text=add_acc_message, parse_mode="html")
    else:
        await message.answer(text=not_admin_message)


@router.message(F.text == "📋 Список аккаунтов")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        accounts_list = await AccountsRepository.find_all()
        formated_list = [
            acc_list_message.format(str(acc.id), acc.username, acc.password, acc.games)
            for acc in accounts_list
        ]
        if len(formated_list):
            for acc in formated_list:
                await message.answer(text=acc)
        else:
            await message.answer(text=empty_acc_list_message)
    else:
        await message.answer(text=not_admin_message)


@router.message(F.text == "📋 Список пользователей")
async def command_admin(message: Message):
    if message.from_user.id == settings.ADMIN_ID:
        users_list = await UsersRepository.find_all()
        formated_list = [
            user_list_message.format(
                str(user.id),
                str(user.tg_id),
                str(user.created_at),
                str(user.last_time_given),
                str(user.is_reffed)
            )
            for user in users_list
        ]
        if len(formated_list):
            for user in formated_list:
                await message.answer(text=user)
        else:
            await message.answer(text=empty_user_list_message)
    else:
        await message.answer(text=not_admin_message)


@router.message(Command("admin"))
async def command_admin(message: Message):
    logger.info("New admin panel request from user: %r", message.from_user.id)
    if message.from_user.id == settings.ADMIN_ID:
        await message.answer(text=admin_panel_message, reply_markup=get_admin_kb())
    else:
        await message.answer(text=not_admin_message)
