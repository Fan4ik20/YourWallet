from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams
from database.interfaces import TransactionsTypesInterface


router = APIRouter(prefix='/transactions/types', tags=['TransactionsTypes'])


@router.get('/', response_model=list[schemas.TransactionsType])
def get_transactions_types(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return TransactionsTypesInterface.get_types(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.TransactionsType,
    status_code=status.HTTP_201_CREATED
)
def create_transactions_type(
        transactions_type: schemas.TransactionsTypeCreate,
        db: Session = Depends(get_db)
):

    errors.raise_bad_request_if_exist_with_name(
        TransactionsTypesInterface.get_type(db, transactions_type.name),
        'TransactionsType'
    )

    return TransactionsTypesInterface.create_type(db, transactions_type)


@router.get(
    '/{transactions_type_name}/',
    response_model=schemas.TransactionsType
)
def get_transactions_type(
        transactions_type_name: schemas.TransactionsTypeEnum,
        db: Session = Depends(get_db)
):
    transactions_type = TransactionsTypesInterface.get_type(
        db, transactions_type_name
    )

    errors.raise_not_found_if_none(transactions_type, 'TransactionsType')

    return transactions_type


@router.delete(
    '/{transactions_type_name}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transactions_type(
        transactions_type_name: schemas.TransactionsTypeEnum,
        db: Session = Depends(get_db)
):
    transactions_type = TransactionsTypesInterface.get_type(
        db, transactions_type_name
    )

    errors.raise_not_found_if_none(transactions_type, 'TransactionsType')

    TransactionsTypesInterface.delete_type(db, transactions_type)
