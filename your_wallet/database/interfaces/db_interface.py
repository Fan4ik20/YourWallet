from database import models, settings


class DbInterface:
    @staticmethod
    def create_tables() -> None:
        models.WalletBase.metadata.create_all(bind=settings.wallet_engine)
