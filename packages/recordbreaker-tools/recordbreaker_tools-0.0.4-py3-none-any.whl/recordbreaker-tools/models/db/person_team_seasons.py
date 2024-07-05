from sqlalchemy import (ForeignKey, Boolean, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class PersonTeamSeasons(CreatedModifiedBase, Base):
    __tablename__ = 'person_team_seasons'
    
    person_team_seasons_id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("people.person_id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    first_name = Column(String)
    last_name = Column(String)
    primary_position = Column(String)
    secondary_position = Column(String)
    role = Column(String, default='PLY')
    red_shirt = Column(Boolean, default=False)
    school_class = Column(String)
    team_sequence = Column(Boolean, primary_key=True)
    season = Column(Integer, primary_key=True)
    season_type = Column(String, primary_key=True)
    jersey_number = Column(Integer)
    short_name = Column(String)
    name = Column(String)
    check_name = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    game_class = Column(String, primary_key=True)

    team = relationship("Teams", foreign_keys=[team_id])
    person = relationship("Person", back_populates="seasons")
    names = relationship("PersonTeamSeasonsNames", back_populates="person_team_season")
