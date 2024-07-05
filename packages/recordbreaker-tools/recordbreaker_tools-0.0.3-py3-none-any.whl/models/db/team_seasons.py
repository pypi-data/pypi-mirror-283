from sqlalchemy import (ForeignKey, Boolean, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class TeamSeasons(CreatedModifiedBase, Base):
    __tablename__ = 'team_seasons'

    team_season_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    season = Column(Integer)
    season_type = Column(String)
    full_name = Column(String)
    conference_id = Column(Integer)
    r_id = Column(String)
    r_abbr = Column(String)
    r_name = Column(String)
    nickname = Column(String)
    division_id = Column(Integer)
    notes = Column(String)
    locale_name = Column(String)
    game_class = Column(String)
    primary_venue = Column(Integer)

    team = relationship("Teams", foreign_keys=[team_id])
