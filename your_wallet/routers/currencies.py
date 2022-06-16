from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams
from database.interfaces.currencies_interface import CurrenciesInterface


router = APIRouter(prefix='/currencies', tags=['Currencies'])


@router.get('/', response_model=list[schemas.Currency])
def get_currencies(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):

    return CurrenciesInterface.get_currencies(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.Currency, status_code=status.HTTP_201_CREATED
)
def create_currency(
        currency: schemas.CurrencyCreate, db: Session = Depends(get_db)
):

    errors.raise_bad_request_if_exist_with_name(
        CurrenciesInterface.get_currency_by_name(db, currency.name), 'Currency'
    )

    return CurrenciesInterface.create_currency(db, currency)


@router.get('/{currency_id}/', response_model=schemas.Currency)
def get_currency(currency_id: int, db: Session = Depends(get_db)):
    currency = CurrenciesInterface.get_currency(db, currency_id)

    errors.raise_not_found_if_none(currency, 'Currency')

    return currency


@router.delete(
    '/{currency_id/}', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    currency = CurrenciesInterface.get_currency(db, currency_id)

    errors.raise_not_found_if_none(currency, 'Currency')

    CurrenciesInterface.delete_currency(db, currency)
