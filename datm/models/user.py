__author__ = 'amar'

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

import base
import artist
import trophy

class User(base.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), index=True, unique=True, nullable=False)

    money = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)

    daily_points = Column(Integer, nullable=False)
    weekly_points = Column(Integer, nullable=False)
    monthly_points = Column(Integer, nullable=False)

    last_reset = Column(Integer)

    artists = relationship(
        "Artist",
        secondary=lambda: assoc_artist_user,
        backref="owners"
    )
    trades = relationship(
        "Trade",
        backref=backref("user", uselist=False)
    )
    trophies = relationship(
        "Trophy",
        secondary=lambda: assoc_trophy_user,
        backref="possessors"
    )

    league_id = Column(Integer, ForeignKey("leagues.id"))

    def __init__(self, name, money, points):
        """Create a new, blank ``User``."""
        self.name = name
        self.money = money
        self.points = points

        self.daily_points = points
        self.weekly_points = points
        self.monthly_points = points

        self.last_reset = None

# FIXME: More magic! Magic!
#           - Create column names from attributes, don't use strings.

assoc_artist_user = Table(
    'assoc_artist_user',
    base.Base.metadata,
    Column('artist_id', String, ForeignKey('artists.mbid')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

assoc_trophy_user = Table(
    'assoc_trophy_user',
    base.Base.metadata,
    Column('trophy_id', Integer, ForeignKey('trophies.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)