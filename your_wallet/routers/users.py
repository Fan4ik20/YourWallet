from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

import schemas
import exc

from dependencies import get_db, PaginationQueryParams
from database.interfaces.users_interface import UsersInterface

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=list[schemas.User])
def get_users(
        pagination_params: PaginationQueryParams = Depends(),
        db: Session = Depends(get_db)
):
    """Pobieranie wszystkich uzytkownikow z bazy danych<br>
    Query parametry:
    - **offset**: odstep od poczatku
    - **limit**: ograniczanie liczby uzytkownikow na jedno zadanie

    """

    return UsersInterface.get_all_users(
        db, pagination_params.offset, pagination_params.limit
    )


@router.post(
    '/', response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Tworzenie uzytkownika z takimi danymi:
    - **username**: obowiazkowe pole
    - **email**: obowiazkowe pole
    - **password**: obowiazkowe pole

    """

    if UsersInterface.get_user_by_username(db, user.username):
        raise exc.ObjectWithGivenAttrExist('User', 'username')

    if UsersInterface.get_user_by_email(db, user.email):
        raise exc.ObjectWithGivenAttrExist('User', 'email')

    return UsersInterface.create_user(db, user)


@router.get('/{user_id}/', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Pobieranie jednego uzytkownika z bazy danych
    Parametry:
    - **user_id**: pole obowiazkowe

    """

    user = UsersInterface.get_user(db, user_id)

    if user is None:
        raise exc.ObjectNotExist('User')

    return user


@router.delete(
    '/{user_id}/', response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Usuwanie uzytwkownika z bazy danych
    Parametry:
    - **user_id**: pole obowiazkowe

    """

    user = UsersInterface.get_user(db, user_id)

    if user is None:
        raise exc.ObjectNotExist('User')

    UsersInterface.delete_user(db, user)
