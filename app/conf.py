# pylint:disable=C0115,C0116,R0903
from datetime import datetime, timedelta

import sqlalchemy as sa
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Env"""

    db_url: PostgresDsn
    secret_key: str
    jwt_claims: dict = {
        "exp": datetime.now() + timedelta(minutes=60),
        "nbf": datetime.now(),
        "iss": "http://localhost:8000",
        "aud": "check",
        "iat": datetime.now(),
    }

    @property
    def engine(self):
        return sa.create_engine(url=self.db_url)

    class Config:
        env_file = ".env"


settings = Settings()
