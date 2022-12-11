from functools import wraps

from fastapi import HTTPException
from pydantic import SecretStr
from sqlalchemy.orm import sessionmaker

from app import settings

SessionLocal = sessionmaker(bind=settings.engine)


def set_session(function):
    """Set Manager()'s session attribute"""

    @wraps(function)
    def wrapper(instance, *args, **kwargs):
        session = SessionLocal()
        try:
            instance.session = session
            call = function(instance, *args, **kwargs)
        finally:
            session.close()
            instance.session = None
        return call

    return wrapper


class Manager:
    """
    Generic class for all commonly used database actions
    """

    def __init__(self) -> None:
        self.session = None
        self._owner = None

    def __set_name__(self, owner, name):
        self._owner = owner

    def _get_query(self):
        if self.session is None:
            raise HTTPException(status_code=400, detail="Session not configure")
        return self.session.query(self._owner)

    @set_session
    def all(self) -> list[object | None]:
        """
        Get a list of model objects

        :return list[object | None]: Extract all rows from database table in the form
        of related model object. Empty list if table is empty
        """
        return self._get_query().all()

    @set_session
    def get(self, **options) -> object:
        """
        Extract object from database based on options

        :params options: one or many possible combination of related model's attribute
        and expected value
        :raises HTTPException: if object not exist in database
        :return object: return object only if `options` matches with database table
        """
        if len(options) == 0:
            raise HTTPException(status_code=400, detail="options cannot be empty")
        instance = self._get_query().filter_by(**options).one_or_none()
        if instance is None:
            raise HTTPException(status_code=404, detail="not found")
        return instance

    @set_session
    def create(self, **options) -> object:
        """
        Save given value as `options` in to corresponding table

        :return object: returns the recently created object
        """
        if len(options) == 0:
            raise HTTPException(status_code=400, detail="options cannot be empty")
        if options.get("id") is not None:
            options.pop("id")
        instance = self._owner(**options)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    @set_session
    def delete(self, **options) -> None:
        """
        Delete row from database table of matching `option`

        :raises HTTPException: _description_
        """
        if len(options) == 0:
            raise HTTPException(status_code=400, detail="options cannot be empty")
        query = self._get_query().filter_by(**options)
        if query.one_or_none() is None:
            raise HTTPException(status_code=404, detail="not found")
        query.delete(synchronize_session=False)
        self.session.commit()


class UserManager(Manager):
    """Inherited form Manager class to perform `User` model specific tasks"""

    def create_user(self, **kwargs):
        """
        - Modified paraent's create() to use in User model
        - focus on hashing password
        """
        raw_password = kwargs.pop("password")
        if isinstance(raw_password, SecretStr):
            raw_password = raw_password.get_secret_value()

        passlib = getattr(self._owner, "hash_password")
        kwargs["password"] = passlib(raw_password)
        return super().create(**kwargs)

    def create_admin(self, **kwargs):
        """
        - Modified paraent's create_user() to use in User model
        - focus on setting `is_admin` attribute to `True`
        """
        kwargs["is_admin"] = True
        return self.create_user(**kwargs)

    def authenticate(self, is_admin=False, **kwargs):
        """useing approprieate credential, check user's existance status

        :param bool is_admin: this key indecate if user is a admin or normal user, defaults to False
        :raises ValueError: if password not provided
        :raises HTTPException: raise if wronge credential user
        :return User: instance of user model
        """

        password = kwargs.pop("password")

        if password is None:
            raise ValueError("password cannot be `None`")

        user = self._owner.objects.get(is_admin=is_admin, **kwargs)

        if not user or not user.check_password(password):
            raise HTTPException(status_code=403, detail="Invalid credential")

        return user
