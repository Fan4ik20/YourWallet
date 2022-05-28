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
    if TransactionsTypesInterface.get_type_by_name(
        db, transactions_type.name
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='TransactionsType with given name already exist'
        )

    return TransactionsTypesInterface.create_type(db, transactions_type)


@router.get(
    '/{transactions_type_id}/',
    response_model=schemas.TransactionsType
)
def get_transactions_type(
        transactions_type_id: int, db: Session = Depends(get_db)
):
    transactions_type = TransactionsTypesInterface.get_type(
        db, transactions_type_id
    )

    errors.raise_not_found_if_none(transactions_type, 'TransactionsType')

    return transactions_type


@router.delete(
    '/{transactions_type_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_transactions_type(
        transactions_type_id: int, db: Session = Depends(get_db)
):
    transactions_type = TransactionsTypesInterface.get_type(
        db, transactions_type_id
    )

    errors.raise_not_found_if_none(transactions_type, 'TransactionsType')

    TransactionsTypesInterface.delete_type(db, transactions_type)
