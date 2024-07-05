from sqlalchemy import (Boolean, Column, DateTime, Integer, String, Time)
from . import CreatedModifiedBase, Base


class Pxp(CreatedModifiedBase, Base):
    __tablename__ = 'pxp'
    
    game_id = Column(Integer, primary_key=True)
    play_id = Column(Integer, primary_key=True)
    drive_id = Column(Integer, primary_key=True)
    drive_play_id = Column(Integer, primary_key=True)
    type = Column(String)
    text = Column(String)
    possession = Column(String)
    down = Column(Integer)
    period = Column(Integer)
    to_go = Column(Integer)
    ball_on = Column(Integer)
    ball_on_after = Column(Integer)
    down_after = Column(Integer)
    to_go_after = Column(Integer)
    possession_after = Column(String)
    yards = Column(Integer)
    is_score = Column(Boolean)
    time = Column(Time)
    score_type = Column(String)
    