from fastapi import APIRouter

from routers import users
from routers import currencies
from routers import user_wallets
from routers.transactions import categories
from routers.transactions import wallet_transactions

router = APIRouter()

router.include_router(users.router)
router.include_router(currencies.router)
router.include_router(user_wallets.router)
router.include_router(categories.router)
router.include_router(wallet_transactions.router)
