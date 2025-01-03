import logging
from datetime import datetime, timedelta

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from src.logs.config import configure_logging
from src.repositories.users_repository import UsersRepository
from src.repositories.accounts_repository import AccountsRepository
from src.models.models import UsersORM, AccountsORM
from src.utils.functions import generate_account
from src.messages.startup_messages import *
from src.middlewares.register_user import RegisterUser
from src.middlewares.check_sub import CheckSubscription


THREE_WEEKS_SECONDS = 1814400

logger = logging.getLogger(__name__)
configure_logging()

router = Router()
router.message.middleware(RegisterUser())
router.message.middleware(CheckSubscription())


@router.message(Command("start"))
async def command_start_handler(message: Message, bot: Bot, command: CommandObject):
    """
    Функция обработки команды /start, для выдачи аккаунтов пользователям бота.
    Здесь реализована основная логика бота

    :param Message message: Сообщение от пользователя
    :param Bot bot: Экземпляр бота
    :param CommandObject command: Экземпляр команды
    :return: None
    """
    logger.info("New request /start from user: %r", message.from_user.id)
    user_tg_id: int = message.from_user.id
    logger.info("User already exists!")
    # Вычисление времени с прошлой раздачи
    current_user_orm: UsersORM = await UsersRepository.find_one_or_none_by_tg_id(tg_id=user_tg_id)
    difference: timedelta = datetime.utcnow() - current_user_orm.last_time_given
    # Проверка возможности получения нового аккаунта
    if current_user_orm.is_possible or difference.total_seconds() >= THREE_WEEKS_SECONDS:
        # Получение аккаунтов пользователя
        users_with_accounts: UsersORM = await UsersRepository.find_one_or_none_by_tg_id_joined(tg_id=user_tg_id)
        users_accounts_list: list[AccountsORM] = users_with_accounts.accounts_got
        # Получение всех аккаунтов
        all_accounts_list: list[AccountsORM] = await AccountsRepository.find_all()
        # Получение id нового аккаунта
        new_user_account_id: int = generate_account(
            users_accounts=users_accounts_list,
            all_accounts=all_accounts_list
        )
        # Проверка на наличие новых аккаунтов
        if new_user_account_id is None:
            await message.answer(text=no_new_acc_yet_message)
            return
        # Добавления нового аккаунта и получение его модели
        new_account_orm: AccountsORM = await UsersRepository.add_user_account(
            tg_id=user_tg_id,
            acc_id=new_user_account_id
        )
        # Доступен и прошло время
        if current_user_orm.is_possible and difference.total_seconds() >= THREE_WEEKS_SECONDS:
            await message.answer(
                parse_mode="html",
                text=give_acc_message.format(
                    new_account_orm.games,
                    new_account_orm.username,
                    new_account_orm.password
                )
            )
            await UsersRepository.update(tg_id=user_tg_id, vals={"is_possible": False})
        # Недоступен и прошло время
        elif not current_user_orm.is_possible and difference.total_seconds() >= THREE_WEEKS_SECONDS:
            await message.answer(
                parse_mode="html",
                text=give_acc_message.format(
                    new_account_orm.games,
                    new_account_orm.username,
                    new_account_orm.password
                )
            )
            await UsersRepository.update(tg_id=user_tg_id, vals={"last_time_given": datetime.utcnow()})
        # Доступен и не прошло время
        elif current_user_orm.is_possible and difference.total_seconds() < THREE_WEEKS_SECONDS:
            await message.answer(
                parse_mode="html",
                text=give_acc_message.format(
                    new_account_orm.games,
                    new_account_orm.username,
                    new_account_orm.password
                )
            )
            await UsersRepository.update(tg_id=user_tg_id, vals={"is_possible": False})
    else:
        await message.answer(text=not_time_yet_message)
