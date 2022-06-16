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
    def get_user_by_username(db: Session, username: str) -> models.User | None:
        return db.scalar(
            select(models.User).filter_by(username=username)
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
