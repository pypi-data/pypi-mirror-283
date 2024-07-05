from sqlalchemy import (ForeignKey, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class TeamNames(CreatedModifiedBase, Base):
    __tablename__ = 'team_names'

    team_name_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    name = Column(String)

    team = relationship("Teams", back_populates='team_names')
