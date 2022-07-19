from typing import Callable

from sqlalchemy.orm import sessionmaker


class WalletDb:
    def __init__(self):
        raise NotImplementedError


def get_db_session(sessionmaker_: sessionmaker) -> Callable:
    def get_db():
        with sessionmaker_() as db:
            yield db

    return get_db()


class PaginationQueryParams:
    def __init__(self, offset: int = 0, limit: int = 100) -> None:
        self.offset = offset
        self.limit = limit
