from pydantic import BaseModel, EmailStr, PositiveInt


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class BaseCurrency(BaseModel):
    name: str


class CurrencyCreate(BaseCurrency):
    pass


class Currency(BaseCurrency):
    id: PositiveInt

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


class TransactionsTypeBase(BaseModel):
    name: str


class TransactionsTypeCreate(TransactionsTypeBase):
    pass


class TransactionsType(TransactionsTypeBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class TransactionsCategoryBase(BaseModel):
    name: str


class TransactionsCategoryCreate(TransactionsCategoryBase):
    pass


class TransactionsCategory(TransactionsCategoryBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    pass


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    class Config:
        orm_mode = True
