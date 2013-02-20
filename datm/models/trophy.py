__author__ = 'amar'

from sqlalchemy import Column, Integer, String

import base
from ..util import db

class Trophy(base.Base):
    __tablename__ = 'trophies'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    desc = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=False)

#   possessors = ... # Many-to-many

    def __init__(self, name, desc, icon):
        """Create a new ``Trophy``, ready to be (but not yet actually) won."""
        self.name = name
        self.desc = desc
        self.icon = icon