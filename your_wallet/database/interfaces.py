from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from database import models

from security import passwords


class UsersInterface:
    @staticmethod
    def get_all_users(
            db: Session, offset: int = 0, limit: int = 100
    ) -> list[models.User]:

        return db.scalars(
            select(models.User).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_user(db: Session, user_id: int) -> models.User | None:
        return db.get(models.User, user_id)

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> models.User | None:
        return db.scalar(
            select(models.User).filter_by(email=email)
        )

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        hashed_password = passwords.get_password_hash(user.password)

        db_user = models.User(
            username=user.username, email=user.email,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()

        db.refresh(db_user)

        return db_user

    @staticmethod
    def delete_user(db: Session, user: models.User) -> None:
        db.delete(user)
        db.commit()


class CurrenciesInterface:
    @staticmethod
    def get_currencies(
            db: Session, offset: int = 0, limit: int = 100
    ) -> list[models.Currency]:

        return db.scalars(
            select(models.Currency).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_currency(db: Session, currency_id: int) -> models.Currency | None:
        return db.get(models.Currency, currency_id)

    @staticmethod
    def get_currency_by_name(db: Session, name: str) -> models.Currency | None:
        return db.scalar(
            select(models.Currency).filter_by(name=name)
        )

    @staticmethod
    def create_currency(
            db: Session, currency: schemas.CurrencyCreate
    ) -> models.Currency:
        db_currency = models.Currency(**currency.dict())

        db.add(db_currency)
        db.commit()

        db.refresh(db_currency)

        return db_currency

    @staticmethod
    def delete_currency(db: Session, currency: models.Currency) -> None:
        db.delete(currency)
        db.commit()


class WalletsInterface:
    @staticmethod
    def get_user_wallets(
            db: Session, user_id: int, offset: int = 0, limit: int = 100
    ) -> list[models.Wallet]:
        return db.scalars(
            select(models.Wallet).filter_by(
                user_id=user_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_user_wallet(
            db: Session, user_id: int, wallet_id: int
    ) -> models.Wallet | None:

        return db.scalar(
            select(models.Wallet).filter_by(id=wallet_id, user_id=user_id)
        )

    @staticmethod
    def create_wallet(
            db: Session, user_id: int, wallet: schemas.WalletCreate
    ) -> models.Wallet:
        db_wallet = models.Wallet(**wallet.dict(), user_id=user_id)

        db.add(db_wallet)
        db.commit()

        db.refresh(db_wallet)

        return db_wallet

    @staticmethod
    def delete_user_wallet(db: Session, wallet: models.Wallet) -> None:
        db.delete(wallet)
        db.commit()


class TransactionsCategoryInterface:
    @staticmethod
    def get_categories(
            db: Session, offset: int = 0, limit: int = 100
    ) -> list[models.TransactionsCategory]:
        return db.scalars(
            select(models.TransactionsCategory).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_category(
            db: Session, transactions_category_id: int
    ) -> models.TransactionsCategory | None:
        return db.get(models.TransactionsCategory, transactions_category_id)

    @staticmethod
    def get_category_by_name(
            db: Session, name: str
    ) -> models.TransactionsCategory | None:

        return db.scalar(
            select(models.TransactionsCategory).filter_by(name=name)
        )

    @staticmethod
    def create_category(
            db: Session,
            transactions_category: schemas.TransactionsCategoryCreate
    ) -> models.TransactionsCategory:
        db_category = models.TransactionsCategory(
            **transactions_category.dict()
        )

        db.add(db_category)
        db.commit()

        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(
            db: Session, transactions_category: models.TransactionsCategory
    ) -> None:
        db.delete(transactions_category)
        db.commit()


class TransactionsTypeInterface:
    @staticmethod
    def get_types(
            db: Session, offset: int = 0, limit: int = 100
    ) -> list[models.TransactionsType]:
        return db.scalars(
            select(models.TransactionsType).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_type(db: Session, type_id: int) -> models.TransactionsType | None:
        return db.get(models.TransactionsType, type_id)

    @staticmethod
    def get_type_by_name(
            db: Session, name: str
    ) -> models.TransactionsType | None:
        return db.scalar(
            select(models.TransactionsType).filter_by(name=name)
        )

    @staticmethod
    def create_type(
            db: Session, transactions_type: schemas.TransactionsTypeCreate
    ) -> models.TransactionsType:
        db_type = models.TransactionsType(**transactions_type.dict())

        db.add(db_type)
        db.commit()

        db.refresh(db_type)
        return db_type

    @staticmethod
    def delete_type(
            db: Session, transactions_type: models.TransactionsType
    ) -> None:
        db.delete(transactions_type)
        db.commit()
