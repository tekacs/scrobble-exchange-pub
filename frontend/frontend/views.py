from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.urlresolvers import reverse

from utils import json_response
from se_api import ttypes

from urllib import quote

NUM_SEARCH_RESULTS = 9
NUM_CHARTS = 5
NUM_LEADERBOARD_ENTRIES = 100
client = settings.CLIENT
TIME_RANGE_TRANSLATION = [0, 31, 7, 1]
#TODO: Handle exceptions with the client


def home(request):
    #Done with the API
    if request.user.is_authenticated():
        authorized_user = _authuser(request)
        user = _user(request)

        api_user_data = client.getUserData(user.name)
        api_user_money = client.getUserMoney(authorized_user)

        user_data = {}
        user_data.update(vars(api_user_data))
        user_data.update(vars(api_user_money))

        user_data['portfolio_worth'] = sum(artist.price for artist in api_user_data.stocks)

        # TODO: Uncomment when the API supports this
        # user_data['recommended_artists'] = client.getTopArtists(NUM_CHARTS, user)
        user_data['recommended_artists'] = {}

        return render_to_response('index.html', {'user_data': user_data}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


def user_profile(request, username):
    return render_to_response('user_profile.html', {}, context_instance=RequestContext(request))


def reset_portfolio(request):
    if not request.user.is_authenticated():
        return redirect('lastfmauth_login', next=request.path)

    if request.method == 'POST':
        #TODO: Reset the user's portfolio
        pass
    else:
        return render_to_response('reset_page.html', {}, context_instance=RequestContext(request))


############ Leaderboards ############
"""By default, show leaderboard that the user is on. Retrieve other leaderboards user requests via AJAX"""
def leaderboards(request):
    leagues = []
    return render_to_response('leaderboards.html', {'leagues': leagues}, context_instance=RequestContext(request))


'''Sample URL: http://localhost:8000/leaderboards/get/user?time_range=3'''
@json_response()
def get_user_leaderboard(request):
    #TODO: Remove return when getNearUsers is implemented in the API
    return {}
    #given: time_range (0-3, 0-alltime, 1-month, 2-week, 3-day)
    unsafe_time_range = int(request.GET.get('time_range', '2'))
    if (unsafe_time_range < len(TIME_RANGE_TRANSLATION)):
        time_range = TIME_RANGE_TRANSLATION[unsafe_time_range]
    else:
        time_range = TIME_RANGE_TRANSLATION[2]

    userdata = client.getUserData(request.user.username)

    user_league = vars(userdata.league)
    user_points = userdata.user.points

    #TODO: Uncomment when its implemented in the API
    # userleaderboard = client.getNearUsers(request.user.username)
    #TODO: Remove magic number and use current position of user instead
    if (userleaderboard.users[3]):
        next_user = vars(userleaderboard.users[3])
    else:
        next_user = {}

    user_position = userleaderboard.position

    data = {
        'user_league': user_league,
        'user_points': user_points,
        'user_position': user_position,
        'next_user': next_user
    }

    return data

'''See http://localhost:8000/leaderboards/get/?league_id=1&time_range=3 for example'''
@json_response()
def get_leaderboard(request):

    league_id = request.GET.get('league_id', 'default_league')
    time_range = TIME_RANGE_TRANSLATION[int(request.GET.get('time_range', '2'))]

    #TODO: Replace magic number for default users
    board = client.getTopUsers(n=NUM_LEADERBOARD_ENTRIES, league=ttypes.League(name=league_id), trange=time_range)

    table = []
    i = 1
    for user in board.users:
        if request.user.is_authenticated() and user.name == request.user.username:
            me = 'me'
        else:
            me = ''

        row = {
            '0': str(i),
            '1': '<a href="www.last.fm/user/{0}"><img src="{1}"/>{0}</a>'.format(user.name, user.profileimage),
            '2': str(user.points),
            'DT_RowClass': 'place-{0} {1}'.format(str(i), me)
        }
        table.append(row)
        i = i + 1

    leaderboard = {
        'sEcho': 1,
        'iTotalRecords': '50',
        'iTotalDisplayRecords': '50',
        'aaData': table
    }

    return leaderboard


############ Artist stuff ############
def artists(request):
    TIME_RANGE = 7
    user = _user(request)

    #TODO: Flatten ArtistSE objects
    top_SE_artists = client.getSETop(NUM_CHARTS,TIME_RANGE, user) #Returns Artists
    top_traded_artists = client.getTradedArtists(NUM_CHARTS, user) #Returns Artists

    # TODO: The API needs to implement this function
    recommended_artists = client.getTopArtists(NUM_CHARTS, user)
    
    popular_LFM_artists = client.getLFMTop(NUM_CHARTS, user)              #Returns Artists
    recently_traded_artists = client.getRecentTrades(NUM_CHARTS, user)    #Returns Artists



    return render_to_response('artists.html', {
        'top_SE_artists': top_SE_artists,
        'top_traded_artists': top_traded_artists,
        'popular_LFM_artists': popular_LFM_artists,
        'recommended_artists': top_artists,
        'recently_traded_artists': recently_traded_artists
    })

def artist_single(request, artistname):
    #TODO: Change artist name mechanism, look at http://stackoverflow.com/a/837835/181284
    
    if (artistname == ''):
        return redirect('artists')

    user = _user(request)

    artist_basic = client.getArtist(ttypes.Artist(mbid = '', name = artistname))

    # Check name and redirect if needed
    if artist_basic.name != artistname:
        return redirect('artist_single', artist_basic, permanent=true)

    artist_se = client.getArtistSE(artist_basic, user)
    artist_lfm = client.getArtistLFM(artist_basic, user)

    returndata = {}
    returndata.update(vars(artist_basic))
    returndata.update(vars(artist_se))
    returndata.update(vars(artist_lfm))

    return render_to_response('artist_single.html', {
        'artist':returndata}, context_instance=RequestContext(request))

''' Sample URL: http://127.0.0.1:8000/artist/history/?artist_id=0383dadf-2a4e-4d10-a46a-e9e041da8eb3&days=2'''
@json_response()
def artist_history(request):
    # artist_id = request.GET.get('artist_id')
    # artist = ttypes.Artist(mbid=artist_id)

    # days = int(request.GET.get('days', '1'))

    # history = client.getArtistHistory(artist, days)

    field = request.GET.get('field', 'money')

    if (field == 'money'):
        history = [
            {
                "name": "price",
                "data": [ { "x": 0, "y": 40 }, { "x": 1, "y": 49 }, { "x": 2, "y": 38 }, { "x": 3, "y": 30 }, { "x": 4, "y": 32 } ]
            }, {
                "name": "dividends",
                "data": [ { "x": 0, "y": 19 }, { "x": 1, "y": 22 }, { "x": 2, "y": 29 }, { "x": 3, "y": 20 }, { "x": 4, "y": 14 } ]
            }
        ]
    elif (field == 'points'):
        history = [
            {
                "name": "points",
                "data": [ { "x": 0, "y": 30 }, { "x": 1, "y": 13 }, { "x": 2, "y": 35 }, { "x": 3, "y": 50 }, { "x": 4, "y": 42 } ]
            }
        ]
    return history

''' Sample URL: http://localhost:8000/search/autocomplete/?q=blah '''
@json_response()
def auto_complete(request):
    #TODO: Change format of data
    partial_text = request.GET.get('q','')
    results = client.searchArtist(partial_text, NUM_SEARCH_RESULTS, 1)
    
    auto = []
    for a in results:
        adict = {
            'value': a.name,
            'url': quote('/artist/'+a.name),
        }
        try:
            adict['img'] = a.imgurls['mega']
        except KeyError:
            pass
        
        auto.append(adict)
        
    return auto

''' Sample URL: http://localhost:8000/search/?q=blah . See https://docs.djangoproject.com/en/dev/topics/forms/ '''
def search(request):
    query = request.GET.get('q','')
    if (query == ''):
        return render_to_response('search_results.html', {
            'query' : '',
            'results' : {},
            'page' : 1,
            'next_page' : "#",
            'previous_page' : "#"
            }, context_instance=RequestContext(request))

    page_number = int(request.GET.get('page', '1'))

    if (page_number > 1):
        previous_page = "%s?q=%s&page=%s" % (reverse('frontend.views.search'), query, page_number - 1)
    else:
        previous_page = "#"
    next_page = "%s?q=%s&page=%s" % (reverse('frontend.views.search'), query, page_number + 1)


    results = client.searchArtist(query, NUM_SEARCH_RESULTS, page_number)
    if not results:
        try:
            results = [client.getArtist(ttypes.Artist(mbid='', name=query))]
        except DataError:
            results = []

    if (request.GET.get('lucky', 'false') == 'true' and results):
        #TODO: Pass ID instead of name once artist_single can handle it
        return redirect('artist_single', results[0].name)
    else:
        return render_to_response('search_results.html', {
            'query':query,
            'results': results,
            'page':page_number,
            'next_page':next_page,
            'previous_page':previous_page}, context_instance=RequestContext(request))


############ Buy/Sell ############

@json_response(auth_needed = True)
def price(request, artist_id=None):
    authorize_ajax_calls(request)

    artist_name = request.GET.get('artist_name')
    artist = ttypes.Artist(name = artist_name)
    authuser =  _authuser(request)
    # artist_SE = client.getArtistSE(artist = artist, user = authuser)
    # TODO: Ask Victor why this may be throwing exceptions
    # Throws errors because the test backend currently only looks stuff up by 
    # artist name
    artist_SE = {
        'artist': {
            'name': 'Coldplay',
            'imgurls': {
                'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/75646980\/Coldplay+PNG.png',
                'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/75646980.png',
                'large': 'http://userserve-ak.last.fm/serve/126/75646980.png',
                'medium': 'http://userserve-ak.last.fm/serve/64/75646980.png',
                'small': 'http://userserve-ak.last.fm/serve/34/75646980.png'
            }
        },
        'price': 2542,
        'points': 242
    }
    return artist_SE

@json_response(auth_needed = True)
def guaranteed_price(request):
    artist_id = request.GET.get('artist_id')
    artist = ttypes.Artist(mbid=artist_id)
    artist_price_guarantee = vars(client.getGuarantee(artist=artist, user=_authuser(request)))
    return artist_price_guarantee

@json_response(auth_needed = True)
@require_POST
def sell(request):
    #TODO: Remind Joe to check out https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    # guarantee = request.POST.get('guarantee')
    elephant = request.POST.get('elephant')
    price = int(request.POST.get('price'))
    time = int(request.POST.get('time'))
    artist = ttypes.Artist(mbid=request.POST.get('artist_id'))

    guarantee = ttypes.Guarantee(elephant = elephant, artist = artist, price = price, time = time)

    success = client.sell(guarantee=guarantee, user=_authuser(request))
    return success

@json_response(auth_needed = True)
@require_POST
def buy(request):
    elephant = request.POST.get('elephant')
    price = int(request.POST.get('price'))
    time = int(request.POST.get('time'))
    artist = ttypes.Artist(mbid=request.POST.get('artist_id'))

    guarantee = ttypes.Guarantee(elephant = elephant, artist = artist, price = price, time = time)

    success = client.buy(guarantee=guarantee, user=_authuser(request))
    return success


############ Helper Functions ############
def _authuser(request):
    if request.user.is_authenticated:
        return ttypes.AuthUser(name=ttypes.User(request.user.username), session_key=request.user.first_name)
    else:
        return None

def _user(request):
    if request.user.is_authenticated:
        return ttypes.User(request.user.username)
    else:
        return ttypes.User('')