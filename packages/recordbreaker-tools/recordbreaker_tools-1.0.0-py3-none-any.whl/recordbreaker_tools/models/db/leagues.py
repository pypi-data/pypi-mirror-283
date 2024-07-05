from sqlalchemy import (Column, DateTime, Integer, String)
from . import Base


class Leagues(Base):
    __tablename__ = 'leagues'

    league_id = Column(Integer, primary_key=True, autoincrement=True)
    league_name = Column(String)
    league_abbr = Column(String)
    common_name = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
 