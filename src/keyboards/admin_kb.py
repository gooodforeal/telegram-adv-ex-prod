from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_kb():
    kb_list = [
        [
            KeyboardButton(text="📋 Список пользователей"),
            KeyboardButton(text="➕ Добавить аккаунт")
        ],
        [
            KeyboardButton(text="📋 Список аккаунтов"),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
