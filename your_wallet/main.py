from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import config
import exc

from database.interfaces.db_interface import DbInterface

from routers import users
from routers import currencies
from routers import user_wallets
from routers.transactions import categories
from routers.transactions import wallet_transactions

app = FastAPI(docs_url='/api/v1/docs/')
DbInterface.create_tables()

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix='/api/v1')
app.include_router(currencies.router, prefix='/api/v1')
app.include_router(user_wallets.router, prefix='/api/v1')
app.include_router(categories.router, prefix='/api/v1')
app.include_router(wallet_transactions.router, prefix='/api/v1')


@app.exception_handler(exc.ObjectNotExist)
def object_not_exist_handler(
        request: Request, exc_: exc.ObjectNotExist
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'message': f'{exc_.model} with given identifier does not exist!'
        }
    )


@app.exception_handler(exc.ObjectWithGivenAttrExist)
def object_with_given_attr_exist_handler(
        request: Request, exc_: exc.ObjectWithGivenAttrExist
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            'message': f'{exc_.model} with given {exc_.attr} already exist'
        }
    )
