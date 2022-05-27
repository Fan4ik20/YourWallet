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
    currency_id: PositiveInt


class WalletCreate(WalletBase):
    pass


class Wallet(WalletBase):
    id: PositiveInt
    user_id: PositiveInt

    class Config:
        orm_mode = True
