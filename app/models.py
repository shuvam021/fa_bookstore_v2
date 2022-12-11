import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from app import settings
from app.utils import JWT, AbstractUser, JWTAud, UserManager

BaseModel = declarative_base(bind=settings.engine)


class User(AbstractUser, BaseModel):
    """User Model"""

    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, index=True, nullable=False)
    username = sa.Column(sa.String(50), unique=True, nullable=True)
    email = sa.Column(sa.String(50), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    is_admin = sa.Column(sa.Boolean, default=False)

    objects = UserManager()

    @property
    def token(self) -> str:
        """custom attribute represents Jason web token"""
        return JWT.encode({"id": self.pk, "aud": JWTAud.LOGIN})
