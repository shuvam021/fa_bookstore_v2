from sqlalchemy.orm import declarative_base

from app.core import settings

BaseModel = declarative_base(bind=settings.engine)
