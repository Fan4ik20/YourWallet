from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

import schemas
from exceptions import exc

from dependencies import WalletDb, PaginationQueryParams

from database.interfaces.wallets_interface import WalletsInterface
from database.interfaces.users_interface import UsersInterface
from database.interfaces.currencies_interface import CurrenciesInterface

router = APIRouter(prefix='/{user_id}/wallets', tags=['Wallets'])


def raise_user_not_exist_if_none(db: Session, user_id: int) -> None:
    user = UsersInterface.get_user(db, user_id)

    if user is None:
        raise exc.ObjectNotExist('User')


@router.get('/', response_model=list[schemas.Wallet])
def get_wallets(
        user_id: int,
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(WalletDb)
):
    raise_user_not_exist_if_none(db, user_id)

    return WalletsInterface.get_user_wallets(
        db, user_id, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.Wallet, status_code=status.HTTP_201_CREATED
)
def create_wallet(
        user_id: int, wallet: schemas.WalletCreate,
        db: Session = Depends(WalletDb)
):
    raise_user_not_exist_if_none(db, user_id)

    if not CurrenciesInterface.get_currency(db, wallet.currency_name):
        raise exc.ObjectNotExist('Currency')

    return WalletsInterface.create_wallet(db, user_id, wallet)


@router.get('/{wallet_id}/', response_model=schemas.Wallet)
def get_wallet(user_id: int, wallet_id: int, db: Session = Depends(WalletDb)):
    raise_user_not_exist_if_none(db, user_id)

    wallet = WalletsInterface.get_user_wallet(db, user_id, wallet_id)

    if wallet is None:
        raise exc.ObjectNotExist('Wallet')

    return wallet


@router.delete(
    '/{wallet_id}/', status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_wallet(
        user_id: int, wallet_id: int, db: Session = Depends(WalletDb)
):
    raise_user_not_exist_if_none(db, user_id)

    wallet = WalletsInterface.get_user_wallet(db, user_id, wallet_id)
    if wallet is None:
        raise exc.ObjectNotExist('Wallet')

    WalletsInterface.delete_user_wallet(db, wallet)
