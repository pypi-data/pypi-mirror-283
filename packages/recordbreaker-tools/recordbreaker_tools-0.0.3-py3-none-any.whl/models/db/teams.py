from sqlalchemy import (Boolean, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class Teams(CreatedModifiedBase, Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    r_id = Column(Integer)
    common_name = Column(String)
    known_names = Column(String)

    team_names = relationship("TeamNames", back_populates="team")
