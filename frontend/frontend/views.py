from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    user_data = __portfolio(request.session['user'])
    return render_to_response('index.html',{user_data = user_data})

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
        return render_to_response('sell.html', {marketprice = marketprice})
    elif (request.POST):
        #TODO: Authenticate
        se_api.create_sell_orders(server=server, 
            user=session['user'], price=price)

def buy_search(request):
    #TODO
    pass

def buy(request, artist=None, artist_id=None, price):
    #TODO
    pass


############ Helper Functions ############

def __portfolio(user=None):
    if (user!=None)
    user_data = se_api.get_user_data(server=server, user=request.session['user'])
    user_data.current_worth = sum(se_api.getArtistData(x).stockvalue
                        for x in user_data.curstocks)
    return user_data

def __authenticated(request):
    if request.session['userapitoken'] == None
    pass