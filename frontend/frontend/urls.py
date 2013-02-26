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

    url(r'^$', 'frontend.views.home', name='home'),
    url(r'^artists/', 'frontend.views.artists', name='artists'),
    url(r'^leaderboards/', 'frontend.views.leaderboards', name='leaderboards'),
    url(r'^sell/', 'frontend.views.sell', name='sell'),
    url(r'^lastfmauth/', include('lastfmauth.urls')),
    url(r'^price/(?P<artist_id>[0-9A-Fa-f-]{36})/$', 'frontend.views.price', name='price'),

    # TODO: need to fix for artists with spaces in names
    url(r'^artist/([^/]+)/$', 'frontend.views.artist_single', name ='artist_single'),

    # (r'^', include(django_url_framework.site.urls) ),
)