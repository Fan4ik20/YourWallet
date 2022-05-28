from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL
from sqlalchemy.orm import declarative_base, relationship, backref

WalletBase = declarative_base()


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


class TransactionType(WalletBase):
    __tablename__ = 'transaction_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)


class TransactionCategory(WalletBase):
    __tablename__ = 'transaction_categories'

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

    transaction_type_id = Column(
        Integer, ForeignKey('transaction_types.id'), nullable=False
    )
    transaction_type = relationship('TransactionType', backref='transactions')

    transaction_category_id = Column(
        Integer, ForeignKey('transaction_categories.id'), nullable=False
    )
    transaction_category = relationship(
        'TransactionCategory', backref='transactions'
    )


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv('../.env')

    from database.settings import wallet_engine

    WalletBase.metadata.create_all(bind=wallet_engine)
