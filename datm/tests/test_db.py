__author__ = 'amar'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Wahey! sys.path munging doesn't work either! :P -- Amar
# (so long as Python thinks of the folder as a subpackage, it won't stop
#  executing its parent's __init__.py - I'll see if I can fix this later.)
#
## Comment on sys.path munging below:
##   Here, sys.path is munged instead of using
##     'from ..models import ...'
##   This is done as a result of Python's module import system.
##
##   If I were to use a relative import, Python would execute datm's
##   __init__.py, which is *not* free from side-effects as it imports
##   all of datm's package-level modules (config, session, etc.)
##
##   Essentially, this means that this test file is isolated from the
##   side-effects and state of the main datm module's (models' parent's)
##   code.
##
##   Please don't change this unless you know exactly what I mean here.
## -- Amar
#
## TODO: See if there's a better way to do this than sys.path munging, whilst
##       still retaining full isolation from parent module's code.
#import sys
#sys.path.append('../models')
#from artist import *
#from internal import *
#from league import *
#from trade import *
#from trophy import *
#from user import *

from ..models.base import Base
from ..models.artist import Artist, ArtistHistory
from ..models.internal import Internal
from ..models.league import League
from ..models.trade import Trade
from ..models.trophy import Trophy
from ..models.user import User

from ..config import DATMConfig
from ..session import DATMSession
from ..util import db

class DatabaseTestBase(object):
    """For tests which require the database and can be run in parallel.

    Uses the standard SQLAlchemy API for setup/teardown (not DATM-internal).
    This exists to verify the functionality of the models independently of the
     ability of DATM to manipulate them using its database access API.
    """

    _multiprocess_shared_ = True

    @classmethod
    def setup_class(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def teardown_class(cls):
        cls.session.close()

class TestModelValidity(DatabaseTestBase):
    """Test that the models are consistent.

    Uses the standard SQLAlchemy API.
    """

    def test_table_consistency(self):
        Base.metadata.create_all(self.engine)
        self.session.flush()

class DATMDBTestBase(object):
    @classmethod
    def setup_class(cls):
        cls.config = DATMConfig(
            db_args={
                'url': 'sqlite:///:memory:',
                'pool_size': None,
                'max_overflow': None
                # SQLite in-memory should be more than sufficient for simplistic
                # model consistency checking, but it doesn't support pooling!
                # Also, this would be best tested against a Postgres instance
                # due to the two databases' different rules, etc.
            }
        )

    @classmethod
    def teardown_class(cls):
        pass

class TestDATMAccess(DATMDBTestBase):
    """Tests the basics of DATM's access to the database using its API.

    This only tests config, session and basic interaction.
    """

    def test_table_creation(self):
        self.config.db.create_all()

    def test_session_instantiation(self):
        with DATMSession(self.config):
            pass

class TestModelFunctionality(DATMDBTestBase):
    """Test that the models behave in the expected fashion with simple flows.

    Uses DATM.
    """
    pass
