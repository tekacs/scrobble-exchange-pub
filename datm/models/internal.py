__author__ = 'amar'

from sqlalchemy import Column, Integer, String

import base

class Internal(base.Base):
    __tablename__ = 'internal'

    id = Column(Integer, primary_key=True)
    secret = Column(String(255), nullable=False)

    # No constructor here - only one instance, which should be instantiated
    # by the default, kwarg'd constructor.
