from sqlalchemy import (Boolean, Column, DateTime, Integer, String, Time)
from . import CreatedModifiedBase, Base


class PxpEvent(CreatedModifiedBase, Base):
    __tablename__ = 'pxp_events'
    
    game_id = Column(Integer, primary_key=True)
    play_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, primary_key=True)
    event_type = Column(String, primary_key=True)
    yards = Column(Integer)
    is_score = Column(Boolean)
    event_subtype = Column(String)
    score_type = Column(String)
    secondary_person_id = Column(Integer)
    inside_20 = Column(Boolean)
    assisted = Column(Boolean)
    period = Column(Integer)
    direction = Column(String)
    in_air = Column(Integer)
    yards_after_catch = Column(Integer)
    