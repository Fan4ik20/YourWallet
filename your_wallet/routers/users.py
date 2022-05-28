from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

import schemas
import errors

from dependencies import get_db, PaginationQueryParams
from database.interfaces import UsersInterface

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[schemas.User])
def get_users(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    return UsersInterface.get_all_users(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db = Depends(get_db)):
    if UsersInterface.get_user_by_email(db, user.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail='Email already registered'
        )

    return UsersInterface.create_user(db, user)


@router.get('/{user_id}/', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UsersInterface.get_user(db, user_id)

    errors.raise_not_found_if_none(user, 'User')

    return user


@router.delete(
    '/{user_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = UsersInterface.get_user(db, user_id)

    errors.raise_not_found_if_none(user, 'User')

    UsersInterface.delete_user(db, user)
