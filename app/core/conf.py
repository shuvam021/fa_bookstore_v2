# pylint:disable=C0115,C0116,R0903
import sqlalchemy as sa
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Env"""

    db_url: PostgresDsn
    secret_key: str

    @property
    def engine(self):
        return sa.create_engine(url=self.db_url)

    class Config:
        env_file = ".env"


settings = Settings()
