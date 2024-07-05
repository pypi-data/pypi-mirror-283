from sqlalchemy import (Boolean, Column, DateTime, Integer, String, Float)
from . import Base
from .game_stats_base import GameStatsBase


class PlayerGameStats(GameStatsBase, Base):
    __tablename__ = 'player_game_stats'

    person_id = Column(Integer, primary_key=True)
    gp = Column(Integer)
    gs = Column(Integer)
    # rcv stats
    rcv_no = Column(Integer)
    rcv_yds = Column(Integer)
    rcv_td = Column(Integer)
    rcv_long = Column(Integer)
    rcv_tgt = Column(Integer)
    # rcv averages
    rcv_avg_yds_att = Column(Float)
    # fr averages
    fr_avg_yds_att = Column(Float)

    
    