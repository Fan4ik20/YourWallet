from sqlalchemy.engine import Engine

from database import models


class DbInterface:
    @staticmethod
    def create_tables(engine: Engine) -> None:
        models.WalletBase.metadata.create_all(bind=engine)
