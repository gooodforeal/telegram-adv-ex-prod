import random
from src.models.models import UsersORM, AccountsORM


def generate_account(users_accounts: list[AccountsORM], all_accounts: list[AccountsORM]) -> int:
    while True:
        if len(users_accounts) == len(all_accounts):
            return 0
        rnd_acc: AccountsORM = random.choice(all_accounts)
        if rnd_acc not in users_accounts:
            return rnd_acc.id
