from sqlalchemy import (Column, DateTime, Integer, String)
from . import Base


class Conferences(Base):
    __tablename__ = 'conferences'

    conference_id = Column(Integer, primary_key=True, autoincrement=True)
    conference_name = Column(String)
    conference_abbr = Column(String)
    common_name = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
