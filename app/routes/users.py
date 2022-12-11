from fastapi import APIRouter
from pydantic import BaseModel as PydanticBM
from pydantic import EmailStr, SecretStr

from app.models import User

router = APIRouter()


class LoginSchema(PydanticBM):
    """Login Serializer"""

    email: EmailStr
    password: str


class UserSchema(PydanticBM):
    """User Serializer"""

    email: EmailStr
    password: SecretStr

    class Config:
        """UserSchema Configuration"""

        orm_mode = True


@router.post("/login", status_code=200, response_model=str)
def login_view(data: LoginSchema):
    """Get all users"""
    user = User.objects.authenticate(**data.dict())
    return user.token


@router.post("/register", status_code=201, response_model=UserSchema)
def register_view(data: UserSchema):
    """Create all users"""
    return User.objects.create_user(**data.dict())
