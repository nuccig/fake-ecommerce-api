from sqlalchemy import Column, Integer  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
