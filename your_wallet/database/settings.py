import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


wallet_engine = create_engine(
    os.getenv('DB_URL')
)

WalletSession = sessionmaker(bind=wallet_engine, autoflush=False)
