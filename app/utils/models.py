# pylint: disable=C0103
from passlib.hash import pbkdf2_sha256


class AbstractModel:
    """Collecection of common feature of a model"""

    @property
    def pk(self):
        """primary key attribute"""
        return self.id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"


class AbstractUser(AbstractModel):
    """Collecection of common feature of a user model"""

    @staticmethod
    def hash_password(raw_password):
        """encrypt raw password"""
        return pbkdf2_sha256.hash(raw_password)

    def check_password(self, raw_password):
        """match raw password with stored encrypted password"""
        return pbkdf2_sha256.verify(raw_password, self.password)
