from sqlalchemy import select
from src.database import async_session_maker
from src.models.models import AccountsORM


class AccountsRepository:
    model = AccountsORM

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int) -> UsersORM:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()