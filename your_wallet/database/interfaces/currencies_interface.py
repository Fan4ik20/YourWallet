from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas

from database import models


class CurrenciesInterface:
    @staticmethod
    def get_currencies(
            db: Session, offset: int = 0, limit: int = 100
    ) -> list[models.Currency]:
        return db.scalars(
            select(models.Currency).offset(offset).limit(limit)
        ).all()

    @staticmethod
    def get_currency(
            db: Session, currency_name: str
    ) -> models.Currency | None:
        return db.get(models.Currency, currency_name)

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
