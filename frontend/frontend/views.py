from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

## Import thrift stuff
import sys
sys.path.append('../../../api/gen-py') #I'm not too sure of this

import se_api
import se_api.ttypes

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
## End of thrift

try:
    ## Connect to the API server
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = se_api.ScrobbleExchange.Client(protocol)
    transport.open()
    ## End
    
    # Now you can access all the thrift stuff
    # To access methods in the ScrobbleExchange service, use
    # client.[servicename](arguments)
    # To create objects as defined in the thrift file
    # Use se_api.[ObjectName]()

    def home(request):
        # user_data = __portfolio(request.session['user'])
        user_data = {}
        return render_to_response('index.html',{'user_data': user_data})

    def artists(request):
        artists = se_api.lastfm.chart.get_top_artists()
        return render_to_response('artists.html', {'artistlist': artists})

    def charts(request):
        return render_to_response('charts.html',{})

    def artist_single(request, artist):
        return render_to_response('artist_single.html', {'name': artist})

    ############ Buy/Sell ############

    def sell(request, artist=None, artist_id=None, price=None):
        if (request.GET or (artist==None and artist_id==None)):
            marketprice = se_api.get_sell_price(artist)
            return render_to_response('sell.html', {'marketprice': marketprice})
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
        pass
    
    # Close
    transport.close()
    
except Thrift.TException, tx:
    print '%s' % (tx.message)
