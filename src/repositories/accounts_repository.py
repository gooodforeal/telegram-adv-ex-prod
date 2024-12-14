from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from src.database import async_session_maker
from src.models.models import AccountsORM


class AccountsRepository:
    model = AccountsORM

    @classmethod
    async def find_all(cls) -> list[AccountsORM]:
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_many(cls, data: list) -> None:
        async with async_session_maker() as session:
            for row in data:
                try:
                    new_account = AccountsORM(**row)
                    session.add(new_account)
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
