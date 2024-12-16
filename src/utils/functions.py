import random
from src.models.models import AccountsORM


def generate_account(users_accounts: list[AccountsORM], all_accounts: list[AccountsORM]) -> int:
    while True:
        # Если список аккаунтов пуст или у пользователя уже есть все доступные аккаунты
        if len(users_accounts) == len(all_accounts) or len(all_accounts) == 0:
            return 0
        rnd_acc: AccountsORM = random.choice(all_accounts)
        if rnd_acc not in users_accounts:
            return rnd_acc.id
