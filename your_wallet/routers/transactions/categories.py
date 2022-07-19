from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from exceptions import exc
import schemas

from dependencies import WalletDb, PaginationQueryParams
from database.interfaces.transactions_categories_interface import (
    TransactionsCategoriesInterface
)

router = APIRouter(
    prefix='/transactions/categories',
    tags=['TransactionsCategories']
)


@router.get('/', response_model=list[schemas.TransactionsCategory])
def get_transactions_categories(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(WalletDb)
):
    return TransactionsCategoriesInterface.get_categories(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.TransactionsCategory,
    status_code=status.HTTP_201_CREATED
)
def create_transactions_category(
        transactions_category: schemas.TransactionsCategoryCreate,
        db: Session = Depends(WalletDb)
):
    if TransactionsCategoriesInterface.get_category(
            db, transactions_category.name
    ):
        raise exc.ObjectWithGivenAttrExist('TransactionsCategory', 'na')

    return TransactionsCategoriesInterface.create_category(
        db, transactions_category
    )


@router.get(
    '/{transactions_category_name}/',
    response_model=schemas.TransactionsCategory
)
def get_transactions_category(
        transactions_category_name: str, db: Session = Depends(WalletDb)
):
    category = TransactionsCategoriesInterface.get_category(
        db, transactions_category_name
    )

    if category is None:
        raise exc.ObjectNotExist('TransactionsCategory')

    return category


@router.delete(
    '/{transactions_category_name}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transactions_category(
        transactions_category_name: str, db: Session = Depends(WalletDb)
):
    category = TransactionsCategoriesInterface.get_category(
        db, transactions_category_name
    )

    if category is None:
        raise exc.ObjectNotExist('TransactionsCategory')

    TransactionsCategoriesInterface.delete_category(
        db, category
    )
