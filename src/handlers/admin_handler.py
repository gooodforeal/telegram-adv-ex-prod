import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.config import settings
from src.logs.config import configure_logging
from src.keyboards.admin_kb import get_admin_kb
from src.models.models import AccountsORM, UsersORM
from src.repositories.users_repository import UsersRepository
from src.repositories.accounts_repository import AccountsRepository
from src.utils.functions import convert_add_message, convert_delete_message
from src.utils.functions import format_users_list, format_accounts_list
from src.messages.admin_messages import *


logger = logging.getLogger(__name__)
configure_logging()

router = Router()


@router.message(
    F.text.startswith(DELETE_ACCOUNT_PATTERN),
    F.from_user.id == settings.ADMIN_ID
)
async def delete_account_handler(message: Message):
    """
    Функция для удаления аккаунта из системы

    :param Message message: Сообщение от пользователя
    :return: None
    """
    try:
        account_dto: dict = convert_delete_message(message=message.text)
        rows_deleted: int = await AccountsRepository.delete(filter_by=account_dto)
        # Проверка количества удаленных записей
        if rows_deleted == 0:
            await message.answer(text=del_acc_not_found)
        else:
            await message.answer(text=success_del_acc_message)
    except Exception as ex:
        logger.error("Invalid data format %s", ex)
        await message.answer(text=invalid_data_message)


@router.message(
    F.text == DELETE_ACCOUNT_INSTRUCTION_PATTERN,
    F.from_user.id == settings.ADMIN_ID
)
async def delete_account_instruction_handler(message: Message):
    """
    Функция для получения инструкции по удаления аккаунта из системы

    :param Message message: Сообщение от пользователя
    :return: None
    """
    await message.answer(text=del_acc_message, parse_mode="html")


@router.message(
    F.text.startswith(ADD_ACCOUNT_PATTERN),
    F.from_user.id == settings.ADMIN_ID
)
async def add_account_handler(message: Message):
    """
    Функция для добавления нового аккаунта в систему

    :param Message message: Сообщение от пользователя
    :return: None
    """
    try:
        account_dto: list[dict] = convert_add_message(message=message.text)
        await AccountsRepository.add_many(data=account_dto)
        await message.answer(text=success_add_acc_message)
    except Exception as ex:
        logger.error("Invalid data format %s", ex)
        await message.answer(text=invalid_data_message)


@router.message(
    F.text == ADD_ACCOUNT_INSTRUCTION_PATTERN,
    F.from_user.id == settings.ADMIN_ID
)
async def add_account_instruction_handler(message: Message):
    """
    Функция для получения инструкции по добавлению нового аккаунта в систему

    :param Message message: Сообщение от пользователя
    :return: None
    """
    await message.answer(text=add_acc_message, parse_mode="html")


@router.message(
    F.text == ACCOUNTS_LIST_PATTERN,
    F.from_user.id == settings.ADMIN_ID
)
async def accounts_list_handler(message: Message):
    """
    Функция для получения списка аккаунтов для выдачи

    :param Message message: Сообщение от пользователя
    :return: None
    """
    accounts_list: list[AccountsORM] = await AccountsRepository.find_all()
    formated_list: list[str] = format_accounts_list(
        pattern=acc_list_message,
        accounts_list=accounts_list
    )
    if len(formated_list):
        for acc in formated_list:
            await message.answer(text=acc)
    else:
        await message.answer(text=empty_acc_list_message)


@router.message(
    F.text == USERS_LIST_PATTERN,
    F.from_user.id == settings.ADMIN_ID
)
async def users_list_handler(message: Message):
    """
    Функция для получения списка пользователей бота

    :param Message message: Сообщение от пользователя
    :return: None
    """
    users_list: list[UsersORM] = await UsersRepository.find_all()
    formated_list: list[str] = format_users_list(
        pattern=user_list_message,
        users_list=users_list
    )
    if len(formated_list):
        for user in formated_list:
            await message.answer(text=user)
    else:
        await message.answer(text=empty_user_list_message)


@router.message(
    Command("admin"),
    F.from_user.id == settings.ADMIN_ID
)
async def command_admin_handler(message: Message):
    """
    Функция обработки команды /admin, которая отдает меню для администратора

    :param Message message: Сообщение от пользователя
    :return: None
    """
    logger.info("New admin panel request from user: %r", message.from_user.id)
    await message.answer(text=admin_panel_message, reply_markup=get_admin_kb())
