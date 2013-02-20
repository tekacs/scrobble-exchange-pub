__author__ = 'amar'

from sqlalchemy import Column, Integer, Boolean, ForeignKey

import base

class Trade(base.Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    purchase = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))