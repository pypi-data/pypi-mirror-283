from sqlalchemy import (Column, DateTime, Integer, Float, String)
from . import CreatedModifiedBase

class ConscGameStatsBase(CreatedModifiedBase, object):
    team_id = Column(Integer, primary_key=True)
    stat_type = Column(String, primary_key=True)
    stat_value = Column(Integer)
    start_game = Column(Integer, primary_key=True)
    end_game = Column(Integer, primary_key=True) # None means it is a current streak
