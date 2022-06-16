from enum import Enum

from pydantic import BaseModel, EmailStr, PositiveInt


def to_camel(string: str) -> str:
    split_string = string.split('_')

    return ''.join(
        [split_string[0]] + [word.capitalize() for word in split_string[1:]]
    )


class LowerCamelCaseBase(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserBase(LowerCamelCaseBase):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class BaseCurrency(LowerCamelCaseBase):
    name: str


class CurrencyCreate(BaseCurrency):
    pass


class Currency(BaseCurrency):
    class Config:
        orm_mode = True


class WalletBase(BaseCurrency):
    name: str
    total_amount: float
    currency_id: PositiveInt | None = None


class WalletCreate(WalletBase):
    pass


class Wallet(WalletBase):
    id: PositiveInt
    user_id: PositiveInt

    class Config:
        orm_mode = True


class TransactionsTypeEnum(Enum):
    outcome = 'outcome'
    income = 'income'


class TransactionsCategoryBase(LowerCamelCaseBase):
    name: str


class TransactionsCategoryCreate(TransactionsCategoryBase):
    pass


class TransactionsCategory(TransactionsCategoryBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class TransactionBase(LowerCamelCaseBase):
    amount: float

    transaction_type: TransactionsTypeEnum
    transaction_category_id: PositiveInt


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: PositiveInt

    wallet_id: PositiveInt

    class Config:
        orm_mode = True
