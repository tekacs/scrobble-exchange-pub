__author__ = 'amar'

from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

import base

class Artist(base.Base):
    __tablename__ = 'artists'

    mbid = Column(String(36), primary_key=True)
    name = Column(String(255), index=True, unique=True, nullable=False)

    lastfm_price = Column(Integer, nullable=False)
    local_price = Column(Integer, nullable=False)
    last_closing_price = Column(Integer, nullable=False)

    max_available = Column(Integer, nullable=False)
#   no_remaining = Column(Integer)

    @hybrid_property
    def no_remaining(self):
        return self.max_available - func.count(self.owners)

#   owners = ... # Many-to-many

    history = relationship("ArtistHistory", backref=backref("artist", uselist=False))

class ArtistHistory(base.Base):
    __tablename__ = 'artist_history'

    date = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

    artist_id = Column(Integer, ForeignKey("artists.mbid"))