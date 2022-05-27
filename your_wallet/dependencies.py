from database.settings import WalletSession


def get_db() -> WalletSession:
    db = WalletSession()

    try:
        yield db
    finally:
        db.close()


class PaginationQueryParams:
    def __init__(self, offset: int = 0, limit: int = 100) -> None:
        self.offset = offset
        self.limit = limit
