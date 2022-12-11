from dataclasses import dataclass

import jwt

from app import settings


@dataclass
class JWTAud:
    """JWTAud"""

    CHECK = "check"
    LOGIN = "login"
    VERIFY = "verify"


class JWT:
    """JWT"""

    @staticmethod
    def _update_claims(payload):
        for k, v in settings.jwt_claims.items():
            if k not in payload:
                payload[k] = v
        return payload

    @classmethod
    def encode(cls, payload: dict) -> str:
        """encode()"""
        payload = cls._update_claims(payload)
        return jwt.encode(payload, settings.secret_key, algorithm="HS256")

    @classmethod
    def decode(cls, token: str, aud: JWTAud) -> dict:
        """decode()"""
        return jwt.decode(
            token, settings.secret_key, algorithms=["HS256"], audience=aud
        )
