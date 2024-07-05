from sqlalchemy import (ForeignKey, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class Venues(CreatedModifiedBase, Base):
    __tablename__ = 'venues'

    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    known_names = Column(String)

    venue_names = relationship("VenueNames", back_populates="venue")

class VenueNames(CreatedModifiedBase, Base):
    __tablename__ = 'venue_names'

    venue_name_id = Column(Integer, primary_key=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey('venues.venue_id'))
    name = Column(String)

    venue = relationship("Venues", back_populates='venue_names')
