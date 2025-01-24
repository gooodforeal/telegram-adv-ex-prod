import logging
import random
from typing import Optional

from src.logs.config import configure_logging
from src.models.models import AccountsORM, UsersORM


logger = logging.getLogger(__name__)
configure_logging()


def generate_account(users_accounts: list[AccountsORM], all_accounts: list[AccountsORM]) -> Optional[int]:
    """
    Функция генерации id нового аккаунта для пользователя с использованием рандома

    :param list[AccountsORM] users_accounts: Список аккаунтов пользователя
    :param list[AccountsORM] all_accounts: Список всех доступных аккаунтов
    :return: int | None: Возвращает id сгенерированного аккаунта
    """
    user_accounts_ids: list[int] = [user.id for user in users_accounts]
    while True:
        # Если список аккаунтов пуст или у пользователя уже есть все доступные аккаунты
        if len(users_accounts) == len(all_accounts) or len(all_accounts) == 0:
            return None
        rnd_acc: AccountsORM = random.choice(all_accounts)
        if rnd_acc.id not in user_accounts_ids:
            return rnd_acc.id


def convert_delete_message(message: str) -> dict:
    """
    Функция для преобразования строкового ввода пользователя по удалению аккаунта в словарь

    :param str message: Сообщение пользователя
    :return: dict: Словарь с информацией от пользователя
    """
    return {"id": int(message.split("\n")[1])}


def convert_add_message(message: str) -> list[dict]:
    """
    Функция для преобразования строкового ввода пользователя по добавлению аккаунта в словарь

    :param str message: Сообщение пользователя
    :return: dict: Словарь с информацией от пользователя
    """
    return [
        {
            "username": acc.split(":")[0],
            "password": acc.split(":")[1],
            "games": acc.split(":")[2]
        }
        for acc in message.split("\n")[1::]
    ]


def format_users_list(pattern: str, users_list: list[UsersORM]) -> list[str]:
    """
    Функция для оформления списка
    сообщений с информацией о пользователях для вывода пользователю

    :param str pattern: Шаблон сообщения
    :param list[UsersORM] users_list: Список моделей с информацией о пользователях
    :return: list[str]: Список сообщений
    """
    return [
        pattern.format(
            str(user.id),
            str(user.tg_id),
            f"@{str(user.username)}",
            str(user.created_at),
            str(user.last_time_given),
            str(user.is_reffed),
            str(len(user.accounts_got))
        )
        for user in users_list
    ]


def format_accounts_list(pattern: str, accounts_list: list[AccountsORM]) -> list[str]:
    """
    Функция для оформления списка
    сообщений с информацией об аккаунтах для вывода пользователю

    :param str pattern: Шаблон сообщения
    :param list[AccountsORM] accounts_list: Список моделей с информацией об аккаунтах
    :return: list[str]: Список сообщений
    """
    return [
        pattern.format(str(acc.id), acc.username, acc.password, acc.games)
        for acc in accounts_list
    ]
