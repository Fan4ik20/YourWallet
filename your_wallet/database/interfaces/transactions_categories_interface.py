from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas

from database import models


class TransactionsCategoriesInterface:
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
