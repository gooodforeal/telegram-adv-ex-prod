from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_kb():
    """
    Функция для получения клавиатуры администратора бота

    :return: ReplyKeyboardMarkup: Клавиатура администратора бота
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Список пользователей")],
            [KeyboardButton(text="📋 Список аккаунтов")],
            [KeyboardButton(text="✅ Добавить аккаунт"), KeyboardButton(text="❌ Удалить аккаунт")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
