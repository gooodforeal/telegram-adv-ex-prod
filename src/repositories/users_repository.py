from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_maker
from src.models.models import UsersORM, AccountsORM


class UsersRepository:
    model = UsersORM

    @classmethod
    async def find_one_or_none_by_tg_id(cls, tg_id: int) -> UsersORM:
        """
        Функция для получения записи из таблицы users по tg_id

        :param int tg_id: Уникальный номер пользователя Telegram
        :return: UsersORM: Модель пользователя
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(tg_id=tg_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_tg_id_joined(cls, tg_id: int) -> UsersORM:
        """
        Функция для получения записи из таблицы users по tg_id с информацией об аккаунтах

        :param int tg_id: Уникальный номер пользователя Telegram
        :return: UsersORM: Модель пользователя
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model).
                options(selectinload(cls.model.accounts_got))
                .filter_by(tg_id=tg_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls) -> list[UsersORM]:
        """
        Функция для получения всех записей из таблицы users

        :return: list[UsersORM]: Список моделей пользователя
        """
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_with_accs(cls) -> list[UsersORM]:
        """
        Функция для получения всех записей из таблицы users c числом аккаунтов

        :return: list[UsersORM]: Список моделей пользователя
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model).
                options(selectinload(cls.model.accounts_got))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_one(cls, tg_id: int, username: str) -> None:
        """
        Функция для добавления новой записи в таблицу users

        :param int tg_id: Уникальный номер пользователя Telegram
        :param str username: Имя пользователя Telegram
        :return: None
        """
        async with async_session_maker() as session:
            try:
                new_user = UsersORM(tg_id=tg_id, username=username)
                session.add(new_user)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def update(cls, tg_id: int, vals: dict = None) -> None:
        """
        Функция для изменения записи в таблице users

        :param int tg_id: Уникальный номер пользователя Telegram
        :param dict vals: Словарь с именованными аргументами для изменения
        :return: None
        """
        async with async_session_maker() as session:
            try:
                stmt = (
                    update(cls.model)
                    .where(cls.model.tg_id == tg_id)
                    .values(**vals)
                )
                res = await session.execute(stmt)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def add_user_account(cls, tg_id: int, acc_id: int) -> Optional[AccountsORM]:
        """
        Функция для добавления нового аккаунта пользователя в таблице users

        :param int tg_id: Уникальный номер пользователя Telegram
        :param int acc_id: Уникальный номер аккаунта
        :return: AccountsORM | None: Возвращает Модель добавленного аккаунта или None
        """
        async with async_session_maker() as session:
            try:
                get_user = (
                    select(cls.model)
                    .filter_by(tg_id=tg_id)
                )
                user_orm: UsersORM = (await session.execute(get_user)).scalar_one()
                get_account = (
                    select(AccountsORM)
                    .filter_by(id=acc_id)
                )
                account_orm: AccountsORM = (await session.execute(get_account)).scalar_one()
                user_orm.accounts_got.append(account_orm)
                await session.commit()
                return account_orm
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
