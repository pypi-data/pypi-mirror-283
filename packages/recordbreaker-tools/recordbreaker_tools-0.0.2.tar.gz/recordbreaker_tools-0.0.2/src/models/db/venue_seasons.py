from sqlalchemy import (ForeignKey, Column, DateTime, Integer, String)
from . import CreatedModifiedBase, Base
from sqlalchemy.orm import relationship


class VenueSeasons(CreatedModifiedBase, Base):
    __tablename__ = 'venue_seasons'

    venue_season_id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer)
    venue_id = Column(Integer, ForeignKey('venues.venue_id'))
    capacity = Column(Integer)
    full_name = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zipcode = Column(String)
    timezone = Column(String)
    season_type = Column(String)
    game_class = Column(String)

    venue = relationship("Venues", foreign_keys=[venue_id])
