from django.conf.urls import patterns, include, url
# from django.conf import settings
# import django_url_framework

# django_url_framework.site.autodiscover(settings.INSTALLED_APPS)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frontend.views.home', name='home'),
    # url(r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #TODO: Remove dollar signs
    url(r'^$', 'frontend.views.home', name='home'),

    # TODO: need to fix for artists with spaces in names
    url(r'^artist/history/', 'frontend.views.artist_history', name='artist_history'),
    url(r'^artist/([^/]*)/?', 'frontend.views.artist_single', name ='artist_single'),
    url(r'^artists/', 'frontend.views.artists', name='artists'),


    url(r'^search/autocomplete', 'frontend.views.auto_complete', name='auto_complete'),
    url(r'^search/', 'frontend.views.search', name='search'),

    url(r'^leaderboards/get/user', 'frontend.views.get_user_leaderboard', name='get_user_leaderboard'),
    url(r'^leaderboards/get', 'frontend.views.get_leaderboard', name='get_leaderboard'),
    url(r'^leaderboards/', 'frontend.views.leaderboards', name='leaderboards'),

    url(r'^sell/', 'frontend.views.sell', name='sell'),
    url(r'^buy/', 'frontend.views.buy', name='buy'),

    url(r'^price/guarantee/', 'frontend.views.guaranteed_price', name='guaranteed_price'),
    url(r'^price/', 'frontend.views.price', name='price'),

    url(r'^lastfmauth/', include('lastfmauth.urls')),

    url(r'^user/([^/]+)/', 'frontend.views.user_profile', name ='user_profile'),
    # (r'^', include(django_url_framework.site.urls) ),
)
