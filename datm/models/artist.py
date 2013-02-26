__author__ = 'amar'

from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

import base

class Artist(base.Base):
    __tablename__ = 'artists'

    mbid = Column(String(36), primary_key=True)
    name = Column(String(255), index=True, unique=True, nullable=False)

    price = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)

    last_closing_price = Column(Integer)
    last_listeners = Column(Integer)
    last_playcount = Column(Integer)

    max_available = Column(Integer, nullable=False)
#   no_remaining = Column(Integer)

    @hybrid_property
    def no_remaining(self):
        return self.max_available - func.count(self.owners)

#   owners = ... # Many-to-many

    trades = relationship(
        "Trade",
        backref=backref("artist", uselist=False)
    )

    history = relationship(
        "ArtistHistory",
        backref=backref("artist", uselist=False)
    )

    def __init__(self, mbid, name, price, points, max_available):
        self.mbid = mbid
        self.name = name

        self.price = price
        self.points = points
        self.max_available = max_available

class ArtistHistory(base.Base):
    __tablename__ = 'artist_history'

    date = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)

    artist_id = Column(Integer, ForeignKey("artists.mbid"))

    def __init__(self, artist, date, price):
        self.artist = artist
        self.date = date
        self.price = price
