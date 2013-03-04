__author__ = 'amar'

from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

import base

class ArtistHistory(base.Base):
    __tablename__ = 'artist_history'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    dividends = Column(Integer, nullable=False)

    artist_id = Column(String(36), ForeignKey("artists.mbid"), index=True)

    def __init__(self, artist, date, price, points, dividends):
        self.artist = artist
        self.date = date
        self.price = price
        self.points = points
        self.dividends = dividends

class Artist(base.Base):
    __tablename__ = 'artists'

    mbid = Column(String(36), primary_key=True)
    name = Column(String(255), index=True, unique=True, nullable=False)

    price = Column(Integer, nullable=False)

    last_closing_price = Column(Integer)
    last_listeners = Column(Integer)
    last_playcount = Column(Integer)

    max_available = Column(Integer, nullable=False)
#   no_remaining = Column(Integer) # Not currently in use.

    @hybrid_property
    def no_remaining(self):
        return self.max_available - len(self.owners)

#   owners = ... # Many-to-many

    trades = relationship(
        "Trade",
        backref=backref("artist", uselist=False)
    )

    history = relationship(
        "ArtistHistory",
        backref=backref("artist", uselist=False),
        order_by=ArtistHistory.date
    )

    def __init__(self, mbid, name, price, max_available):
        self.mbid = mbid
        self.name = name

        self.price = price
        self.max_available = max_available

        self.last_closing_price = price
