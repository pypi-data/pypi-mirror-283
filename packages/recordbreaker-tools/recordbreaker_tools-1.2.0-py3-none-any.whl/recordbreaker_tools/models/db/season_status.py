from sqlalchemy import (Boolean, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class SeasonStatus(CreatedModifiedBase, Base):
    __tablename__ = 'season_status'

    date_of_games = Column(DateTime, primary_key=True)
    season = Column(Integer)
    season_type = Column(String)
    game_class = Column(String)
    games_processed = Column(Boolean)
