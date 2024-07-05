from sqlalchemy import (Boolean, Column, DateTime, Integer, String)
from . import Base
from .game_stats_base import GameStatsBase
from sqlalchemy.orm import relationship


class TeamGameStats(GameStatsBase, Base):
    __tablename__ = 'team_game_stats'

    firstdowns_no = Column(Integer)
    firstdowns_pass = Column(Integer)
    firstdowns_rush = Column(Integer)
    firstdowns_penalty = Column(Integer)
    penalties_no = Column(Integer)
    penalties_yds = Column(Integer)
    conversions_thirdconv = Column(Integer)
    conversions_thirdatt = Column(Integer)
    conversions_fourthconv = Column(Integer)
    conversions_fourthatt = Column(Integer)
    time_of_poss = Column(Integer)
    redzone_att = Column(Integer)
    redzone_scores = Column(Integer)
    redzone_points = Column(Integer)
    redzone_tdrush = Column(Integer)
    redzone_tdpass = Column(Integer)
    redzone_fgmade = Column(Integer)
    redzone_endfga = Column(Integer)
    redzone_enddowns = Column(Integer)
    redzone_endint = Column(Integer)
    redzone_endfumb = Column(Integer)
    redzone_endhalf = Column(Integer)
    redzone_endgame = Column(Integer)
    misc_yds = Column(Integer)
    misc_top = Column(String)
    misc_ona = Column(Integer)
    misc_onm = Column(Integer)
    misc_ptsto = Column(Integer)

    team = relationship("Teams", back_populates="game_stats")
