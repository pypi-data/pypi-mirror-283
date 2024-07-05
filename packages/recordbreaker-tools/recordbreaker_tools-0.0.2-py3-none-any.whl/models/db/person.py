from sqlalchemy import (Boolean, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class Person(CreatedModifiedBase, Base):
    __tablename__ = 'people'

    person_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    birthdate = Column(DateTime)
    hometown_country = Column(String)
    hometown_city = Column(String)
    hometown_state = Column(String)
    high_school_id = Column(Integer)
    high_school_country = Column(String)
    high_school_city = Column(String)
    high_school_state = Column(String)
    high_school_name = Column(String)
    college_id = Column(Integer)
    college_country = Column(String)
    college_city = Column(String)
    college_state = Column(String)
    college_name = Column(String)
    r_id = Column(Integer)

    seasons = relationship("PersonTeamSeasons", back_populates="person")
