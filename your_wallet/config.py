from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv('.env')


class AppSettings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
