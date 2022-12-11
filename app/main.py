from enum import Enum

from fastapi import FastAPI

from app.routes import users

app = FastAPI(title="Bookstore Api", version="0.1", description=None)


class URLTags(str, Enum):
    """a class that collect all url tags for swagger ui"""

    HOME = "Home"
    AUTH = "Authentication"


@app.get("/", response_model=dict, tags=[URLTags.HOME])
def root():
    """test api"""
    return {"message": "welcome to bookstore service"}


app.include_router(router=users.router, prefix="/auth", tags=[URLTags.AUTH])
