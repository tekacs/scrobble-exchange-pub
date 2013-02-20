"""A simple harness to help test DATM from the REPL."""

from sqlalchemy import func

from datm import *
from datm.models import *
from datm.util import db, magic

config = DATMConfig(
    db_args={
        'url': 'sqlite:///:memory:',
        'pool_size': None,
        'max_overflow': None
    }
)

session = DATMSession(config)
session.bind()

config.db.create_all()