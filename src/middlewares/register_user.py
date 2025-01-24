import logging
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.utils.payload import decode_payload

from src.logs.config import configure_logging
from src.models.models import UsersORM
from src.repositories.users_repository import UsersRepository

logger = logging.getLogger(__name__)
configure_logging()


class RegisterUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger.info("User registration start! User: %r", event.from_user.id)
        user_tg_id: int = event.from_user.id
        username: str = event.from_user.username
        command: CommandObject = data["command"]
        user_exists_check: UsersORM = await UsersRepository.find_one_or_none_by_tg_id(tg_id=user_tg_id)
        if not user_exists_check:
            logger.info("Adding new user to database")
            await UsersRepository.add_one(tg_id=user_tg_id, username=username)
            # Получение аргументов реферальной ссылки
            if command.args:
                payload: int = int(decode_payload(command.args))
                referral_user_orm: UsersORM = await UsersRepository.find_one_or_none_by_tg_id(tg_id=payload)
                # Проверка на то, что пользователь еще не реферал
                if not referral_user_orm.is_reffed:
                    await UsersRepository.update(tg_id=payload, vals={"is_reffed": True, "is_possible": True})
        return await handler(event, data)
