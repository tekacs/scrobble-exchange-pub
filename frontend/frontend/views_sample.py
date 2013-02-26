from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
import models
from utils import json_response

import random

# Import thrift stuff

import sys, glob
sys.path.append('/home/mtkl/test/gen-py')

from se_api import ScrobbleExchange
from se_api import ttypes

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
# End of thrift



def home(request):
    
    try:
        # Connect to the API server
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = ScrobbleExchange.Client(protocol)
        transport.open()
        # End

        #Done with the API
        api_user_data = client.getUserData('fiwl')
        authorized_user = ttypes.AuthUser(name = ttypes.User(name = 'fiwl'), 
            session_key = 'thekeyyougot')
        
        user_data = models.UserData()
        user_data.stocks = []
        for artistse in api_user_data.stocks:
            a = {'name': artistse.artist.name, 'imgurls': 
                                                        artistse.artist.imgurls}
            user_data.stocks.append({'artist': a, 'price': artistse.price})
        user_data.user = {'money': client.getUserMoney(authorized_user).money, 
                        'points': api_user_data.user.points}
        user_data.portfolio_worth = sum(artist.price for artist in 
                                                        api_user_data.stocks)
        
        # Close
        transport.close()
        
        return render_to_response('index.html',
        {'user_data': user_data}, context_instance=RequestContext(request)
        )
        
    except Thrift.TException, tx:
        print '%s' % (tx.message)
      
def artists(request):
    
    try:
        # Connect to the API server
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = ScrobbleExchange.Client(protocol)
        transport.open()
        # End

        authorized_user = ttypes.AuthUser(name = ttypes.User(name = 'fiwl'), 
                                                session_key = 'thekeyyougot')
        artist1 = ttypes.Artist(name = 'Iron Maiden')
        artist2 = ttypes.Artist(name = 'Foo Fighters')
        artistlist = [artist1, artist2]

        api_top_artists = client.getSETop(5)
        top_SE_artists = []
        for i in api_top_artists:
            a = client.getArtistSE(i, authorized_user)
            artist = {'name': i.name, 'imgurls': i.imgurls}
            top_SE_artists.append({'artist':artist, 'price': a.price, 'points': 
            a.points})
        
        rising_SE_artists = list(top_SE_artists)
        random.shuffle(rising_SE_artists)
        
        recommended_artists = list(top_SE_artists)
        random.shuffle(recommended_artists)
        
        # Close
        transport.close()
        
        return render_to_response('artists.html', {
            'artistlist': artistlist, 
            'top_SE_artists': top_SE_artists, 
            'top_LFM_artists': reversed(top_SE_artists), 
            'rising_SE_artists': rising_SE_artists,
            'recommended_artists': recommended_artists
            })
        
    except Thrift.TException, tx:
        print '%s' % (tx.message)

def leaderboards(request):
    return render_to_response('leaderboards.html',{}, 
                                context_instance=RequestContext(request))

def get_leaderboard(request):
    pass

def search(request):
    pass

def auto_complete(request):
    pass

def artist_single(request, artistname):
    
    try:
        # Connect to the API server
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = ScrobbleExchange.Client(protocol)
        transport.open()
        # End
    
        #Done with the API
        authorized_user = ttypes.AuthUser(name = ttypes.User(name = 'fiwl'), 
                                                session_key = 'thekeyyougot')
        artist_basic = client.getArtist(ttypes.Artist(mbid = '', name = 
                        artistname))
        artist_se = client.getArtistSE(artist_basic, authorized_user)
        artist_lfm = client.getArtistLFM(artist_basic)
        
        artist = {'name':artist_basic.name, 
                'bio':{'summary': artist_lfm.bio.summary}, 'similar': 
                artist_lfm.similar}
        
        artist_sse = {'artist': artist, 'ownedby': artist_se.ownedby, 
                    'price': artist_se.price}
        
        return render_to_response('artist_single.html', {
            'artist_SE':artist_sse}, context_instance=RequestContext(request))
    
    except Thrift.TException, tx:
        print '%s' % (tx.message)
    
############ Buy/Sell ############
@json_response
def price(request, artist_id=None):
    print 'entered price function correctly'
    # artist_SE = client.getArtistSE(artist = se_api.Artist(mbid = artist_id), user = request.user)
    artist_price_guarantee = client.getGuarantee(artist = se_api.Artist(mbid = artist_id), user = request.user)
    return artist_price_guarantee


@json_response
def sell(request, artist=None, artist_id=None, price=None):
    if (request.GET or (artist==None and artist_id==None)):
        #marketprice = se_api.get_sell_price(artist)
        marketprice = 40
        return {'marketprice': 40}
        #return render_to_response('sell.html', {'marketprice': 
#marketprice})
    elif (request.POST):
        pass
        #TODO: Authenticate
        # if 'user' in request.session:
        #     se_api.create_sell_orders(server=server, 
        #         user=request.session['user'], price=price)

def buy_search(request):
    #TODO
    pass

def buy(request, artist=None, artist_id=None, price=None):
    #TODO
    pass

############ Helper Functions ############

def __portfolio(user=None):
    if user is not None:
        user_data = se_api.get_user_data(server=server, user=user)
        user_data.current_worth = sum(se_api.getArtistData(x).stockvalue
                            for x in user_data.curstocks)
    return user_data

def __authenticated(request):
    #if request.session['userapitoken'] is not None:
    return {}
