__author__ = 'amar'

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

import base

class League(base.Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True, unique=True, nullable=False)
    desc = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=False)

    users = relationship(
        "User",
        backref=backref("league", uselist=False)
    )

    def __init__(self, name, desc, icon):
        """Create a new, empty ``League``, ready to contain ``User``s."""
        self.name = name
        self.desc = desc
        self.icon = icon