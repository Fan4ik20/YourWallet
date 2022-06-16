from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams
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
        db: Session = Depends(get_db)
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
        db: Session = Depends(get_db)
):

    errors.raise_bad_request_if_exist_with_name(
        TransactionsCategoriesInterface.get_category_by_name(
            db, transactions_category.name
        ), 'TransactionsCategory'
    )

    return TransactionsCategoriesInterface.create_category(
        db, transactions_category
    )


@router.get(
    '/{transactions_category_id}/', response_model=schemas.TransactionsCategory
)
def get_transactions_category(
        transactions_category_id: int, db: Session = Depends(get_db)
):
    category = TransactionsCategoriesInterface.get_category(
        db, transactions_category_id
    )

    errors.raise_not_found_if_none(category, 'TransactionsCategory')

    return category


@router.delete(
    '/{transactions_category_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transactions_category(
        transactions_category_id: int, db: Session = Depends(get_db)
):
    category = TransactionsCategoriesInterface.get_category(
        db, transactions_category_id
    )

    errors.raise_not_found_if_none(category, 'TransactionsCategory')

    TransactionsCategoriesInterface.delete_category(
        db, category
    )
