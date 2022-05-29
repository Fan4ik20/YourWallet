from fastapi import FastAPI

import config


from routers import users
from routers import currencies
from routers import user_wallets
from routers.transactions import categories
from routers.transactions import wallet_transactions


app = FastAPI(docs_url='/api/v1/docs/')

app.include_router(users.router, prefix='/api/v1')
app.include_router(currencies.router, prefix='/api/v1')
app.include_router(user_wallets.router, prefix='/api/v1')
app.include_router(categories.router, prefix='/api/v1')
app.include_router(wallet_transactions.router, prefix='/api/v1')
