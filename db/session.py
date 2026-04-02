from os import getenv
import pathlib

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

BASE_URL = pathlib.Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=BASE_URL.joinpath('.env/db.env'))

    def get_db_url_pg(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings() # type: ignore
print(settings.get_db_url_pg())
engine = create_engine(url=settings.get_db_url_pg(), echo=True)

session = sessionmaker(bind=engine, expire_on_commit=False)
