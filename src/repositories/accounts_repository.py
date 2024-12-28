from typing import Optional

from sqlalchemy import select
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_maker
from src.models.models import AccountsORM


class AccountsRepository:
    model = AccountsORM

    @classmethod
    async def find_all(cls) -> list[AccountsORM]:
        """
        Функция для получения всех записей из таблицы accounts

        :return: list[AccountsORM]: Список моделей ORM
        """
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_many(cls, data: list[dict]) -> None:
        """
        Функция для добавления нескольких записей в таблицу accounts

        :param list[dict] data: Список словарей с информацией об аккаунтах
        :return: None
        """
        async with async_session_maker() as session:
            for row in data:
                try:
                    new_account = AccountsORM(**row)
                    session.add(new_account)
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    @classmethod
    async def delete(cls, filter_by: dict) -> Optional[int]:
        """
        Функция удаляет записи из таблицы по указанному фильтру

        :param dict filter_by: Словарь с фильтрами
        :return: int | None: Возвращает количество удаленных строк или None
        """
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
