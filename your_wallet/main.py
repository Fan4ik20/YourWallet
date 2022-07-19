from typing import TypeAlias

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exceptions import handlers, exc

from database.settings import create_db_engine, create_sessionmaker
from database.interfaces.db_interface import DbInterface

from dependencies import WalletDb, get_db_session

from routers import wallet_router

from config import AppSettings

url: TypeAlias = str


def include_routers(app_: FastAPI) -> None:
    app_.include_router(wallet_router.router, prefix='/api/v1')


def include_handlers(app_: FastAPI) -> None:
    app_.add_exception_handler(
        exc.ObjectNotExist, handlers.object_not_exist_handler
    )
    app_.add_exception_handler(
        exc.ObjectNotExistInBody, handlers.object_not_exist_handler
    )
    app_.add_exception_handler(
        exc.ObjectWithGivenAttrExist,
        handlers.object_with_given_attr_exist_handler
    )


def include_cors(app_: FastAPI, origins: list[url]) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_db(app_: FastAPI, config: AppSettings) -> None:
    wallet_engine = create_db_engine(config)
    wallet_sessionmaker = create_sessionmaker(wallet_engine)

    DbInterface.create_tables(wallet_engine)

    app_.dependency_overrides[WalletDb] = get_db_session(wallet_sessionmaker)


def create_app() -> FastAPI:
    wallet_app = FastAPI(docs_url='/api/v1/docs/', debug=True)
    wallet_settings = AppSettings(_env_file='.env')

    origins = [
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ]

    include_db(wallet_app, wallet_settings)
    include_handlers(wallet_app)
    include_cors(wallet_app, origins)
    include_routers(wallet_app)

    return wallet_app


app = create_app()
