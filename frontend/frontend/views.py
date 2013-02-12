from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
import models
from utils import json_response

## Import thrift stuff
#import sys
#sys.path.append('../../../api/gen-py') # Variable depending on install

#from se_api import ScrobbleExchange
#import se_api.ttypes

#from thrift import Thrift
#from thrift.transport import TSocket
#from thrift.transport import TTransport
#from thrift.protocol import TBinaryProtocol
## End of thrift

#try:
    ## Connect to the API server
    #transport = TSocket.TSocket('localhost', 9090)
    #transport = TTransport.TBufferedTransport(transport)
    #protocol = TBinaryProtocol.TBinaryProtocol(transport)
    #client = ScrobbleExchange.Client(protocol)
    #transport.open()
    ## End
    
    # Now you can access all the thrift stuff
    # To access methods in the ScrobbleExchange service, use
    # client.[servicename](arguments)
    # To create objects as defined in the thrift file
    # Use se_api.[ObjectName]()

def home(request):
    # user_data = __portfolio(request.session['user'])
    # user_data.worth = sum(se_api.getArtistData(x).stockvalue
    #                         for x in user_data.curstocks)

    # Dummy artist data
    user_data = models.UserData()
    user_data.curstocks = [
        {
            'artist': {
                'name': 'Coldplay',
                'current_price': 2500,
                'images': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/75646980\/Coldplay+PNG.png',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/75646980.png'
                    # in real data, get all available image urls
                }
            }
        }, 
        {
            'artist': {
                'name': 'Daft Punk',
                'current_price': 2200,
                'images': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/4183432\/Daft+Punk+daftpunk_1.jpg',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/4183432.jpg'    
                    # in real data, get all available image urls
                }
            }
        },
        {
            'artist': {
                'name': 'Gorillaz',
                'current_price': 2300,
                'images': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/_\/411274\/Gorillaz.jpg',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/411274.jpg'    
                    # in real data, get all available image urls
                }
            }
        }
    ]
    user_data.user = {'money': 140512}
    portfolio_worth = 2500 + 2200 + 2300
    return render_to_response('index.html',{
            'user_data': user_data, 
            'portfolio_worth': portfolio_worth
        })

def artists(request):
    # artistlist = se_api.lastfm.chart.get_top_artists()
    artist1 = models.Artist()
    artist1.name = 'Iron Maiden'
    artist2 = models.Artist()
    artist2.name = 'Foo Fighters'
    artistlist = [artist1, artist2]
    return render_to_response('artists.html', {'artistlist': artistlist})

def leaderboards(request):
    return render_to_response('leaderboards.html',{})

def artist_single(request, artist):
    artist = type('Artist', (), {'name': artist})();
    return render_to_response('artist_single.html', {'artist': artist})

############ Buy/Sell ############

@json_response
def sell(request, artist=None, artist_id=None, price=None):
    if (request.GET or (artist==None and artist_id==None)):
        #marketprice = se_api.get_sell_price(artist)
        marketprice = 40
        return {'marketprice': 40}
        #return render_to_response('sell.html', {'marketprice': marketprice})
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

# Close
# transport.close()
    
# except Thrift.TException, tx:
#     print '%s' % (tx.message)
