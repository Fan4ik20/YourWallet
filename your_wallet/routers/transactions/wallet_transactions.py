from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams

from database.interfaces.transactions_interface import TransactionsInterface
from database.interfaces.users_interface import UsersInterface
from database.interfaces.wallets_interface import WalletsInterface
from database.interfaces.transactions_categories_interface import (
    TransactionsCategoriesInterface
)


router = APIRouter(
    prefix='/{user_id}/{wallet_id}/transactions', tags=['Transactions']
)


def raise_404_if_user_or_wallet_is_none(
        db: Session, user_id: int, wallet_id: int
) -> None:
    user = UsersInterface.get_user(db, user_id)
    errors.raise_not_found_if_none(user, 'User')

    wallet = WalletsInterface.get_user_wallet(db, user_id, wallet_id)
    errors.raise_not_found_if_none(wallet, 'Wallet')


def raise_422_if_transactions_category_id_not_valid(
        db: Session, category_id: int
) -> None:
    category = TransactionsCategoriesInterface.get_category(db, category_id)

    if category is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Transactions Category with given id does not exist',
        )


@router.get('/', response_model=list[schemas.Transaction])
def get_transactions(
        user_id: int, wallet_id: int,
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    raise_404_if_user_or_wallet_is_none(db, user_id, wallet_id)

    return TransactionsInterface.get_transactions(
        db, user_id, wallet_id,
        pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.Transaction,
    status_code=status.HTTP_201_CREATED
)
def create_transaction(
        user_id: int, wallet_id: int, transaction: schemas.TransactionCreate,
        db: Session = Depends(get_db)
):
    raise_404_if_user_or_wallet_is_none(db, user_id, wallet_id)
    raise_422_if_transactions_category_id_not_valid(
        db, transaction.transaction_category_id
    )

    return TransactionsInterface.create_transaction(
        db, wallet_id, transaction
    )


@router.get('/{transaction_id}/', response_model=schemas.Transaction)
def get_transaction(
        user_id: int, wallet_id: int, transaction_id: int,
        db: Session = Depends(get_db)
):
    raise_404_if_user_or_wallet_is_none(db, user_id, wallet_id)

    transaction = TransactionsInterface.get_transaction(
        db, user_id, wallet_id, transaction_id
    )

    errors.raise_not_found_if_none(transaction, 'Transaction')

    return transaction


@router.delete(
    '/{transaction_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transaction(
        user_id: int, wallet_id: int, transaction_id: int,
        db: Session = Depends(get_db)
):
    raise_404_if_user_or_wallet_is_none(db, user_id, wallet_id)

    transaction = TransactionsInterface.get_transaction(
        db, user_id, wallet_id, transaction_id
    )
    errors.raise_not_found_if_none(transaction, 'Transaction')

    TransactionsInterface.delete_transaction(db, transaction)
