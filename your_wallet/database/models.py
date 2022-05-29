from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, Enum
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.orm.decl_api import DeclarativeMeta

from schemas import TransactionsTypeEnum

WalletBase: DeclarativeMeta = declarative_base()


class User(WalletBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(70), unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)


class Currency(WalletBase):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False, unique=True)


class Wallet(WalletBase):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)

    name = Column(String(35), nullable=True)

    total_amount = Column(DECIMAL, nullable=False, default=0)

    user_id = Column(
        Integer, ForeignKey('users.id'), nullable=False
    )
    user = relationship(
        'User', backref=backref('wallets', cascade='all, delete-orphan')
    )

    currency_id = Column(Integer, ForeignKey('currencies.id'))
    currency = relationship('Currency', backref='wallets')


class TransactionsCategory(WalletBase):
    __tablename__ = 'transactions_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)


class Transaction(WalletBase):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)

    amount = Column(DECIMAL, nullable=False)

    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    wallet = relationship(
        'Wallet', backref=backref('transactions', cascade='all, delete-orphan')
    )

    transaction_type = Column(
        Enum(TransactionsTypeEnum), nullable=False
    )

    transaction_category_id = Column(
        Integer, ForeignKey('transactions_categories.id'), nullable=False
    )
    transaction_category = relationship(
        'TransactionsCategory', backref='transactions'
    )


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv('../.env')

    from database.settings import wallet_engine

    WalletBase.metadata.create_all(bind=wallet_engine)
