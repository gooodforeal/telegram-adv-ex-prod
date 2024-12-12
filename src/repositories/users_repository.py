from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from src.database import async_session_maker
from src.models.models import UsersORM


class UsersRepository:
    model = UsersORM

    @classmethod
    async def find_one_or_none_by_tg_id(cls, tg_id: int) -> UsersORM:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(tg_id=tg_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls) -> list[UsersORM]:
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_one(cls, tg_id: int) -> None:
        async with async_session_maker() as session:
            try:
                new_user = UsersORM(tg_id=tg_id)
                session.add(new_user)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

    @classmethod
    async def update(cls, tg_id: int, vals: dict = None) -> None:
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
