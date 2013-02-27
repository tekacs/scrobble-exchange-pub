__author__ = 'amar'

from sqlalchemy import Column, Integer, String

import base
from ..util import db

class Trophy(base.Base):
    __tablename__ = 'trophies'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
    icon = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

#   possessors = ... # Many-to-many

    def __init__(self, name, icon, description):
        """Create a new ``Trophy``, ready to be (but not yet actually) won."""
        self.name = name
        self.icon = icon
        self.description = description
