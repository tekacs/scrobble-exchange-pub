# Python Server

import sys
sys.path.append('gen-py')

from se_api import ScrobbleExchange
from se_api.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

#import datm

class SEHandler(object):
    #config = datm.DATMConfig(api_key=api_key, db_url='postgres://url')
    
    def login(self, token):
    """
    If successful, returns the user token. If not, returns an
    AuthException. AccountException is returned if account data is
    incorrect or doesn't exist, and should be handled appropriately

    Parameters:
     - token
    """
    pass

    def getArtist(self, artist):
    """
    Returns basic artist info. Artist string can be either the name, or the
    musicbrainz ID

    Parameters:
     - artist
    """
   
    #if artist.mbid != '':
        #a = datm.Artist(config, mbid = artist.mbid)
    #else if artist.name != '':
        #a = datm.Artist(config, name = artist.name)
    #else:
        #raise SearchException("Incorrect artist data")
    
    #ret = Artist()
    #ret.mbid = a.mbid
    #ret.name = a.name
    #ret.imageurl = a.images
    
    #return ret
    pass

  def getLightArtist(self, artist):
    """
    Returns only MusicBrainz ID and name

    Parameters:
     - artist
    """
    #if artist.mbid != '':
        #a = datm.Artist(config, mbid = artist.mbid)
    #else if artist.name != '':
        #a = datm.Artist(config, name = artist.name)
    #else:
        #raise SearchException("Incorrect artist data")
    
    #ret = Artist()
    #ret.mbid = a.mbid
    #ret.name = a.name
    
    #return ret
    pass

  def getArtistSE(self, artist):
    """
    Returns the data from our db for the artist.
    Assumes that if artist isn't in the DB, then it gets pulled in
    on-demand and so will always return some data.
    Artist string can be either the name, or the musicbrainz ID

    Parameters:
     - artist
    """
    #if artist.mbid != '':
        #a = datm.Artist(config, mbid = artist.mbid)
    #else if artist.name != '':
        #a = datm.Artist(config, name = artist.name)
    #else:
        #raise SearchException("Incorrect artist data")
    
    #ret = Artist()
    #ret.mbid = a.mbid
    #ret.name = a.name
    #ret.imageurl = a.images
    #ret.price = a.price
    #ret.num_remaining = a.no_remaining
    
    #return ret
    pass

  def getArtistLFM(self, artist):
    """
    Returns the contextual artist info from last.fm for the artist
    Artist string can be either the name or the musicbrainz ID

    Parameters:
     - artist
    """
    pass

  def searchArtist(self, text):
    """
    returns a list of possible artists from a partial string. Ordered by
    decreasing relevance. List size is limited to 5 elements.

    Parameters:
     - text
    """
    pass

  def getTopArtists(self, n, tag):
    """
    Returns a list of the n top artists by decreasing value. By default, tag
    should have a value of '' and only be used if you want to limit the
    top lists to a certain tag.

    Parameters:
     - n
     - tag
    """
    pass

  def getTradedArtists(self, n):
    """
    Returns a list of the n most traded artists by decreasing value.

    Parameters:
     - n
    """
    pass

  def getUserData(self, user):
    """
    Returns extended user data for the current user

    Parameters:
     - user
    """
    pass

  def getUserInfo(self, user):
    """
    Returns extended user data for the user in the string. Mostly, used for
    profile pages

    Parameters:
     - user
    """
    pass

  def getTopUsers(self, n, league):
    """
    Returns the n top users by decreasing value in the given league.

    Parameters:
     - n
     - league
    """
    pass

  def getNearUsers(self, user):
    """
    Returns a list of 10 users with 4 above and 5 below in the leaderboard
    compared to the user provided

    Parameters:
     - user
    """
    pass

  def getTransaction(self, artist):
    """
    Returns the guarantee token to the front end

    Parameters:
     - artist
    """
    pass

  def buyArtist(self, transaction, user):
    """
    Buys artist for user, and returns the new value of that stock in the
    game. Throws a transaction exception if something goes wrong while
    buying or the user can't afford to buy the artist.
    Throws user exception if the user already owns the stock

    Parameters:
     - transaction
     - user
    """
    pass

  def sellArtist(self, transaction, user):
    """
    Sells artist for user, and returns the new value of that artist. User
    exception is thrown if the user isn't allowed to sell or doesn't own
    that artist

    Parameters:
     - transaction
     - user
    """
    pass

processor = ScrobbleExchange.Process(SEHandler())
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
