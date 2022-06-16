from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from schemas import TransactionsTypeEnum

from database import models


class TransactionsInterface:
    @staticmethod
    def _get_filtered_select_with_joins(user_id: int, wallet_id: int):
        return select(
            models.Transaction
        ).join(models.Wallet).join(
            models.User
        ).filter(
            models.User.id == user_id, models.Wallet.id == wallet_id
        )

    @staticmethod
    def get_transactions(
            db: Session, user_id: int, wallet_id: int,
            offset: int = 0, limit: int = 100,
    ) -> models.Transaction:
        return db.scalars(
            TransactionsInterface._get_filtered_select_with_joins(
                user_id, wallet_id
            ).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_transaction(
            db: Session, user_id: int, wallet_id: int,
            transaction_id: int
    ) -> models.Transaction | None:
        return db.scalar(
            TransactionsInterface._get_filtered_select_with_joins(
                user_id, wallet_id
            ).filter(models.Transaction.id == transaction_id)
        )

    @staticmethod
    def _change_wallet_total_amount(
            wallet: models.Wallet, transaction_type: TransactionsTypeEnum,
            amount: float
    ) -> None:

        if transaction_type == TransactionsTypeEnum.outcome:
            wallet.total_amount -= amount
        elif transaction_type == TransactionsTypeEnum.income:
            wallet.total_amount += amount

    @staticmethod
    def _create_transaction_object(
            db: Session, wallet_id: int, transaction: schemas.TransactionCreate
    ) -> models.Transaction:
        new_transaction = models.Transaction(
            **transaction.dict(), wallet_id=wallet_id
        )

        db.add(new_transaction)
        db.commit()

        db.refresh(new_transaction)

        return new_transaction

    @staticmethod
    def _change_wallet_total_amount_after_creating(
            db: Session, transaction: models.Transaction
    ) -> None:
        TransactionsInterface._change_wallet_total_amount(
            transaction.wallet, transaction.transaction_type,
            transaction.amount
        )
        db.commit()

    @staticmethod
    def create_transaction(
            db: Session, wallet_id: int,
            transaction: schemas.TransactionCreate
    ) -> models.Transaction:
        new_transaction = TransactionsInterface._create_transaction_object(
            db, wallet_id, transaction
        )

        TransactionsInterface._change_wallet_total_amount_after_creating(
            db, new_transaction
        )

        return new_transaction

    @staticmethod
    def _change_wallet_total_amount_before_deleting(
            db: Session, transaction: models.Transaction
    ) -> None:
        type_name = transaction.transaction_type

        reversed_type_name = (
            TransactionsTypeEnum.income
            if type_name == TransactionsTypeEnum.outcome
            else TransactionsTypeEnum.outcome
        )

        TransactionsInterface._change_wallet_total_amount(
            transaction.wallet, reversed_type_name, transaction.amount
        )

        db.commit()

    @staticmethod
    def delete_transaction(
            db: Session, transaction: models.Transaction
    ) -> None:
        TransactionsInterface._change_wallet_total_amount_before_deleting(
            db, transaction
        )

        db.delete(transaction)
        db.commit()
