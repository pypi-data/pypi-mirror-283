from sqlalchemy import (Boolean, Column, DateTime, Integer, String, text)
from . import CreatedModifiedBase, Base


class GameDrive(CreatedModifiedBase, Base):
    __tablename__ = 'game_drives'

    game_id = Column(Integer, primary_key=True)
    drive_id = Column(Integer, primary_key=True)
    possession = Column(Integer)
    start_how = Column(String)
    start_period = Column(Integer)
    start_time = Column(String)
    start_ball_on = Column(Integer)
    end_how = Column(String)
    end_period = Column(Integer)
    end_time = Column(String)
    end_ball_on = Column(Integer)
    plays = Column(Integer)
    yards = Column(Integer)
    time_of_possession = Column(String)
    redzone = Column(Integer)
