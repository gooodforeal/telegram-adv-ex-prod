from datetime import datetime

from sqlalchemy import ForeignKey, func, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, int_pk


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    tg_id: Mapped[str]
    username: Mapped[str] = mapped_column(nullable=True)
    last_time_given: Mapped[datetime] = mapped_column(server_default=func.now())
    is_reffed: Mapped[bool] = mapped_column(default=False)
    is_possible: Mapped[bool] = mapped_column(default=True)

    accounts_got: Mapped[list["AccountsORM"]] = relationship(
        back_populates="users_got",
        secondary="users_accounts",
        lazy="selectin"
    )

    extend_existing = True


class AccountsORM(Base):
    __tablename__ = "accounts"

    id: Mapped[int_pk]
    username: Mapped[str]
    password: Mapped[str]
    games: Mapped[str]

    users_got: Mapped[list["UsersORM"]] = relationship(
        back_populates="accounts_got",
        secondary="users_accounts",
        lazy="selectin"
    )

    extend_existing = True


class UsersAccounts(Base):
    __tablename__ = "users_accounts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        primary_key=True,
    )
