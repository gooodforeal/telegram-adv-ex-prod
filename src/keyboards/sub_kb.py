from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.config import settings


def get_sub_kb() -> InlineKeyboardMarkup:
    """
    Функция для получения клавиатуры подписки на канал

    :return: InlineKeyboardMarkup: Клавиатура подписки на канал
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться", url=settings.CHANNEL_LINK)
            ]
        ]
    )
