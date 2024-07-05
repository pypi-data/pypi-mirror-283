from sqlalchemy import (ForeignKey, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class PersonTeamSeasonsNames(CreatedModifiedBase, Base):
    __tablename__ = 'person_team_seasons_names'
    
    person_team_seasons_names_id = Column(Integer, primary_key=True)
    person_team_seasons_id = Column(Integer, ForeignKey("person_team_seasons.person_team_seasons_id"))
    checkname = Column(String)
    shortname = Column(String)

    person_team_season = relationship("PersonTeamSeasons", back_populates="names")
