from sqlalchemy import (Column, DateTime, Integer, Float)
from .consc_game_stats_base import ConscGameStatsBase

class PlayerConscGameStats(ConscGameStatsBase):
    __tablename__ = 'player_consc_game_stats'

    player_id = Column(Integer, primary_key=True)
