from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams
from database.interfaces import WalletsInterface, UsersInterface

router = APIRouter(prefix='/{user_id}/wallets', tags=['wallets'])


def raise_404_if_user_not_exist(db: Session, user_id: int) -> None:
    user = UsersInterface.get_user(db, user_id)

    errors.raise_not_found_if_none(user, 'User')


@router.get('/', response_model=list[schemas.Wallet])
def get_wallets(
        user_id: int,
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    raise_404_if_user_not_exist(db, user_id)

    return WalletsInterface.get_user_wallets(
        db, user_id, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.Wallet, status_code=status.HTTP_201_CREATED
)
def create_wallet(
        user_id: int, wallet: schemas.WalletCreate,
        db: Session = Depends(get_db)
):
    raise_404_if_user_not_exist(db, user_id)

    return WalletsInterface.create_wallet(db, user_id, wallet)


@router.get('/{wallet_id}/', response_model=schemas.Wallet)
def get_wallet(user_id: int, wallet_id: int, db: Session = Depends(get_db)):
    raise_404_if_user_not_exist(db, user_id)

    wallet = WalletsInterface.get_user_wallet(db, user_id, wallet_id)

    errors.raise_not_found_if_none(wallet, 'Wallet')

    return wallet


@router.delete(
    '/{wallet_id}/', status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
def delete_wallet(user_id: int, wallet_id: int, db: Session = Depends(get_db)):
    raise_404_if_user_not_exist(db, user_id)

    wallet = WalletsInterface.get_user_wallet(db, user_id, wallet_id)
    errors.raise_not_found_if_none(wallet, 'Wallet')

    WalletsInterface.delete_user_wallet(db, wallet)
