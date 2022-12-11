from enum import Enum

from fastapi import FastAPI

app = FastAPI(title="Bookstore Api", version="0.1", description=None)


class URLTags(str, Enum):
    """a class that collect all url tags for swagger ui"""

    HOME = "Home"


@app.get("/", response_model=dict, tags=[URLTags.HOME])
def root():
    """test api"""
    return {"message": "welcome to bookstore service"}
