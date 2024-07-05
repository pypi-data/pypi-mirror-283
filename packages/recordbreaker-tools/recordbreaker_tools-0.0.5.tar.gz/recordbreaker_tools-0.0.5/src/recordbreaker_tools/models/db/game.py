from sqlalchemy import (Boolean, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base


class Game(CreatedModifiedBase, Base):
    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True, autoincrement=False)
    tgt_id = Column(Integer)
    opp_id = Column(Integer)
    tgt_abbr = Column(String)
    opp_abbr = Column(String)
    home = Column(Integer)
    visitors = Column(Integer)
    home_score = Column(Integer)
    visitors_score = Column(Integer)
    tgt_score = Column(Integer)
    opp_score = Column(Integer)
    date = Column(DateTime)
    date_display = Column(String)
    attendance = Column(Integer)
    venue_id = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    weather = Column(String)
    leaguegame = Column(Boolean)
    tgt_rank = Column(Integer)
    opp_rank = Column(Integer)
    game_class = Column(String)
    season_type = Column(String)
    season = Column(Integer)
    result = Column(String)
    disposition = Column(String)
    url = Column(String)
    byu_game_nid = Column(Integer)
    day_night = Column(String)
    surface = Column(String)
    periods = Column(Integer)

    def __str__(self):
        return f'{self.game_id} {self.game_class} {self.teams}'
