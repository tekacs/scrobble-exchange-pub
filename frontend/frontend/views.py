from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.urlresolvers import reverse

from utils import json_response
from se_api import ttypes

NUM_SEARCH_RESULTS = 9
NUM_CHARTS = 5
NUM_LEADERBOARD_ENTRIES = 100
TIME_RANGE_TRANSLATION = [0, 31, 7, 1]
client = settings.CLIENT


def home(request):
    #Done with the API
    if request.user.is_authenticated():
        authorized_user = _authuser(request)
        api_user_data = client.getUserData(authorized_user.user.name)
        request.user.portfolio_worth = sum(artist.price for artist in api_user_data.stocks)

        try:
            request.user.recommended_artists = client.getTopArtists(NUM_CHARTS, authorized_user.user)
        except Exception:
            request.user.recommended_artists = {}

        return render_to_response('index.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response('welcome.html', {}, context_instance=RequestContext(request))


# @contextmanager
# def handler():
#     try:
#         yield
#     except TTransportException:
#         def inner(*args, **kwargs):
#             return {}
#         return inner


# def _wrap(method):
#     def fn(*args, **kwargs):
#         try:
#             return method(*args, **kwargs)
#         except TTransportException:
#             return {}
#     return fn


def user_profile(request, username):
    # No user profiles as of now
    return render_to_response('user_profile.html', {}, context_instance=RequestContext(request))


def reset_portfolio(request):
    if not request.user.is_authenticated():
        return redirect('lastfmauth_login', next=request.path)

    authorized_user = _authuser(request)
    if request.method == 'POST':
        success = client.reset(authorized_user)
        return render_to_response('reset_page.html', {'success': success}, context_instance=RequestContext(request))
    else:
        return render_to_response('reset_page.html', {'success': 'Unsubmitted'}, context_instance=RequestContext(request))


############ Leaderboards ############
def leaderboards(request):
    """Empty leaderboards page with list of leagues. Actual data retrieved by AJAX"""
    leagues = client.getLeagues()
    return render_to_response('leaderboards.html', {'leagues': leagues}, context_instance=RequestContext(request))


@json_response()
def get_user_leaderboard(request):
    """Sample URL: http://localhost:8000/leaderboards/get/user?time_range=3"""

    #given: time_range (0-3, 0-alltime, 1-month, 2-week, 3-day)
    unsafe_time_range = int(request.GET.get('time_range', '2'))
    if (unsafe_time_range < len(TIME_RANGE_TRANSLATION)):
        time_range = TIME_RANGE_TRANSLATION[unsafe_time_range]
    else:
        time_range = TIME_RANGE_TRANSLATION[2]

    userdata = client.getUserData(request.user.username)

    user_league = vars(userdata.league)
    user_points = userdata.user.points

    #TODO: Needs to be implemented in the API
    userleaderboard = client.getNearUsers(request.user.username, time_range)
    user_position = userleaderboard.position
    if (userleaderboard.users[user_position - 1]):
        next_user = vars(userleaderboard.users[user_position - 1])
    else:
        next_user = {}

    data = {
        'user_league': user_league,
        'user_points': user_points,
        'user_position': user_position,
        'next_user': next_user
    }

    return data


@json_response()
def get_leaderboard(request):
    """Sample URL: http://localhost:8000/leaderboards/get/?league_name=1&time_range=3"""
    league_name = request.GET.get('league_name', 'default_league')
    time_range = TIME_RANGE_TRANSLATION[int(request.GET.get('time_range', '2'))]

    board = client.getTopUsers(n=NUM_LEADERBOARD_ENTRIES, league=ttypes.League(name=league_name), trange=time_range)

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

    top_SE_artists = _flattenArtistSEList(client.getSETop(NUM_CHARTS, TIME_RANGE, user))
    top_traded_artists = _flattenArtistSEList(client.getTradedArtists(NUM_CHARTS, user))
    recommended_artists = _flattenArtistSEList(client.getTopArtists(NUM_CHARTS, user))  # TODO: The API needs to implement this function
    popular_LFM_artists = _flattenArtistSEList(client.getLFMTop(NUM_CHARTS, user))
    recently_traded_artists = _flattenArtistSEList(client.getRecentTrades(NUM_CHARTS, user))

    return render_to_response('artists.html', {
        'top_SE_artists': top_SE_artists,
        'top_traded_artists': top_traded_artists,
        'recommended_artists': recommended_artists,
        'popular_LFM_artists': popular_LFM_artists,
        'recently_traded_artists': recently_traded_artists
    })


def artist_single(request, artistname):
    if (artistname == ''):
        return redirect('artists')

    user = _user(request)

    artist_basic = client.getArtist(ttypes.Artist(mbid='', name=artistname))

    # Check name and redirect if needed
    if artist_basic.name != artistname:
        return redirect('artist_single', artist_basic, permanent=True)

    artist_se = client.getArtistSE(artist_basic, user)
    artist_lfm = client.getArtistLFM(artist_basic)

    returndata = {}
    returndata.update(vars(artist_basic))
    returndata.update(vars(artist_se))
    returndata.update(vars(artist_lfm))

    return render_to_response('artist_single.html', {
        'artist': returndata}, context_instance=RequestContext(request))


@json_response()
def artist_history(request):
    """ Sample URL: http://127.0.0.1:8000/artist/history/?artist_id=0383dadf-2a4e-4d10-a46a-e9e041da8eb3&days=2"""

    def _format(megadict):
        data = []
        for time, value in megadict:
            data.append({"x": time, "y": value})
        return data

    artist_id = request.GET.get('artist_id')
    artist = ttypes.Artist(mbid=artist_id)

    days = int(request.GET.get('days', '1'))

    full_history = client.getArtistHistory(artist, days)

    field = request.GET.get('field', 'money')

    if (field == 'money'):
        req_history = [
            {
                "name": "price",
                "data": _format(full_history.histprices)
            }, {
                "name": "dividends",
                "data": _format(full_history.histdividends)
            }
        ]
    elif (field == 'points'):
        req_history = [
            {
                "name": "points",
                "data": _format(full_history.histpoints)
            }
        ]
    return req_history


@json_response()
def auto_complete(request):
    """ Sample URL: http://localhost:8000/search/autocomplete/?q=blah """
    partial_text = request.GET.get('q', '')
    results = _filterInvalidArtists(client.searchArtist(partial_text, NUM_SEARCH_RESULTS, 1))

    auto = []
    for artist in results:
        adict = {
            'value': artist.name,
            'url': reverse('artist_single', args=(artist.name,))
        }
        try:
            adict['img'] = artist.imgurls['mega']
        except KeyError:
            pass

        auto.append(adict)

    return auto


def search(request):
    """ Sample URL: http://localhost:8000/search/?q=blah . """
    query = request.GET.get('q', '')

    #If no search has been made, return empty search page
    if (query == ''):
        return render_to_response('search_results.html', {
            'query': '',
            'results': {},
            'page': 1,
            'next_page': "#",
            'previous_page': "#"
        }, context_instance=RequestContext(request))

    #Pagination
    page_number = int(request.GET.get('page', '1'))

    if (page_number > 1):
        previous_page = "%s?q=%s&page=%s" % (reverse('frontend.views.search'), query, page_number - 1)
    else:
        previous_page = "#"
    next_page = "%s?q=%s&page=%s" % (reverse('frontend.views.search'), query, page_number + 1)

    #Search results, which may need to be autocorrected
    results = _filterInvalidArtists(client.searchArtist(query, NUM_SEARCH_RESULTS, page_number))
    if not results:
        try:
            results = [client.getArtist(ttypes.Artist(mbid='', name=query))]
        except ttypes.DataError:
            results = []

    if (request.GET.get('lucky', 'false') == 'true' and results):
        #TODO: Pass ID instead of name once artist_single can handle it
        return redirect('artist_single', results[0].name)
    else:
        return render_to_response('search_results.html', {
            'query': query,
            'results': results,
            'page': page_number,
            'next_page': next_page,
            'previous_page': previous_page}, context_instance=RequestContext(request))


def _filterInvalidArtists(artists):
    return [artist for artist in artists if artist.mbid is not None]

############ Buy/Sell ############


@json_response(auth_needed=True)
def price(request, artist_id=None):
    artist_name = request.GET.get('artist_name')
    artist = ttypes.Artist(name=artist_name)
    user = _user(request)

    artist = _flattenArtistSE(client.getArtistSE(artist=artist, user=user))
    return artist


@json_response(auth_needed=True)
def guaranteed_price(request):
    artist_id = request.GET.get('artist_id')
    artist = ttypes.Artist(mbid=artist_id)
    artist_price_guarantee = vars(client.getGuarantee(artist=artist, user=_authuser(request)))
    return artist_price_guarantee


@json_response(auth_needed=True)
@require_POST
def sell(request):
    #TODO: Remind Joe to check out https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    elephant = request.POST.get('elephant')
    price = int(request.POST.get('price'))
    time = int(request.POST.get('time'))
    artist = ttypes.Artist(mbid=request.POST.get('artist_id'))

    guarantee = ttypes.Guarantee(elephant=elephant, artist=artist, price=price, time=time)

    success = client.sell(guarantee=guarantee, user=_authuser(request))
    return success


@json_response(auth_needed=True)
@require_POST
def buy(request):
    elephant = request.POST.get('elephant')
    price = int(request.POST.get('price'))
    time = int(request.POST.get('time'))
    artist = ttypes.Artist(mbid=request.POST.get('artist_id'))

    guarantee = ttypes.Guarantee(elephant=elephant, artist=artist, price=price, time=time)

    success = client.buy(guarantee=guarantee, user=_authuser(request))
    return success


############ Helper Functions ############
def _authuser(request):
    if request.user.is_authenticated:
        authuser = ttypes.AuthUser(user=ttypes.User(request.user.username), session_key=request.user.first_name)
        updatedauthuser = client.getUserMoney(authuser)
        request.user.points = updatedauthuser.user.points
        request.user.money = updatedauthuser.money
        return updatedauthuser
    else:
        return None


def _user(request):
    if request.user.is_authenticated:
        return ttypes.User(request.user.username)
    else:
        return ttypes.User('')


def _flattenArtistSEList(artists):
    artistdicts = []
    for artistSE in artists:
        artistdicts.append(_flattenArtistSE(artistSE))


def _flattenArtistSE(artistSE):
    artistdict = {}
    artistdict.update(vars(artistSE))
    artistdict.update(vars(artistSE.artist))
    return artistdict
