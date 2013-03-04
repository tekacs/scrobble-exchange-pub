__author__ = 'amar'

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

import base

class Trade(base.Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    purchase = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    artist_id = Column(String, ForeignKey("artists.mbid"))

    def __init__(self, user, artist, price, purchase, date):
        """Create new ``Trade`` for ``user``, of ``artist``, at ``price``."""
        self.user = user
        self.artist = artist
        self.price = price
        self.purchase = purchase
        self.date = date
