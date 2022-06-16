from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

import schemas
import exc

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


def raise_user_or_wallet_not_exist_if_none(
        db: Session, user_id: int, wallet_id: int
) -> None:
    user = UsersInterface.get_user(db, user_id)
    if user is None:
        raise exc.ObjectNotExist('User')

    wallet = WalletsInterface.get_user_wallet(db, user_id, wallet_id)
    if wallet is None:
        raise exc.ObjectNotExist('Wallet')


def raise_category_not_exist_if_none(db: Session, category_name: str):
    category = TransactionsCategoriesInterface.get_category(db, category_name)
    if category is None:
        raise exc.ObjectNotExistInBody('TransactionsCategory')


@router.get('/', response_model=list[schemas.Transaction])
def get_transactions(
        user_id: int, wallet_id: int,
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    raise_user_or_wallet_not_exist_if_none(db, user_id, wallet_id)

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
    raise_user_or_wallet_not_exist_if_none(db, user_id, wallet_id)
    raise_category_not_exist_if_none(db, transaction.transaction_category_name)

    return TransactionsInterface.create_transaction(
        db, wallet_id, transaction
    )


@router.get('/{transaction_id}/', response_model=schemas.Transaction)
def get_transaction(
        user_id: int, wallet_id: int, transaction_id: int,
        db: Session = Depends(get_db)
):
    raise_user_or_wallet_not_exist_if_none(db, user_id, wallet_id)

    transaction = TransactionsInterface.get_transaction(
        db, user_id, wallet_id, transaction_id
    )

    if transaction is None:
        raise exc.ObjectNotExist('Transactions')

    return transaction


@router.delete(
    '/{transaction_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transaction(
        user_id: int, wallet_id: int, transaction_id: int,
        db: Session = Depends(get_db)
):
    raise_user_or_wallet_not_exist_if_none(db, user_id, wallet_id)

    transaction = TransactionsInterface.get_transaction(
        db, user_id, wallet_id, transaction_id
    )
    if transaction is None:
        raise exc.ObjectNotExist('Transactions')

    TransactionsInterface.delete_transaction(db, transaction)
