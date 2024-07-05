from sqlalchemy import (Column, ForeignKey, Integer, Float)
from . import Base
from .game_stats_base import GameStatsBase
from sqlalchemy.orm import relationship


class PlayerGameStats(GameStatsBase, Base):
    __tablename__ = 'player_game_stats'

    person_id = Column(Integer, ForeignKey("people.person_id"), primary_key=True)
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

    person = relationship("Person", back_populates="game_stats")
    