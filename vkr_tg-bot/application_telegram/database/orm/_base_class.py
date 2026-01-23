from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from datetime import datetime


metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    metadata = metadata_obj
