from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas

from database import models


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
