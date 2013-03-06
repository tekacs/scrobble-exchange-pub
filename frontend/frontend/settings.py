# Django settings for frontend project.

import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Import thrift stuff
from se_api import ScrobbleExchange, ttypes
from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
# End of thrift

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Team Charlie', 'scrobbleexchange-all@srcf.net'),
)

#superuser - supercharlie, supercharliepass
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'scrobblefront.db',                 # Or path to database file if using sqlite3.
        'USER': 'charlie',                          # Not used with sqlite3.
        'PASSWORD': 'myritylv',                     # Not used with sqlite3.
        'HOST': '',                                 # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                 # Set to empty string for default. Not used with sqlite3.
    }
}

API_SERVER = 'ec2-54-246-25-244.eu-west-1.compute.amazonaws.com'
# API_SERVER = 'localhost'
API_PORT = 9090

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://44db69ee886344a8a3aff3163c6f81da:231dfa61bb6f4b8aa33ebcb65ecff701@app.getsentry.com/6005',
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#=*qsr310y#ixy8r6)0bz-y#p%aakdfws1a#4+_h397e4^k$wt'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'frontend.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'frontend.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    'lastfmauth',
    'raven.contrib.django.raven_compat',
    #'frontendapp',
    # 'django_url_framework',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTHENTICATION_BACKENDS = (
    'lastfmauth.backends.LastfmAuthBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "frontend.utils.get_current_path",
)

#TODO: Add database table name prefix to avoid collisions with rest of data

import os
from functools import wraps as _wraps

def new_pipe():
    try:
        transport = TSocket.TSocket(API_SERVER, API_PORT)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = ScrobbleExchange.Client(protocol)
        transport.open()
        return client
    except Thrift.TException, tx:
        print '%s' % (tx.message)
CLIENT_BUILDER = new_pipe

class ClientProxy(object):
    def __init__(self, client_builder, exceptions):
        self._client = client_builder()
        self._client_builder = client_builder
        self._exceptions = exceptions

    def __getattr__(self, name):
        if self._client is None:
            self._client = self._client_builder()
        attr = getattr(self._client, name)
        if not callable(attr):
            return attr
        @_wraps(attr)
        def rebuilder(*args, **kwargs):
            try:
                return attr(*args, **kwargs)
            except self._exceptions as e:
                print "Repaired broken pipe due to %s" % e
                self._client = self._client_builder()
                return getattr(self._client, name)(*args, **kwargs)
        return rebuilder

CLIENT = ClientProxy(new_pipe, (ttypes.TException, os.error))

LASTFM_API_KEY = CLIENT.apikey()
LASTFM_WS_BASE_URL = "http://ws.audioscrobbler.com/2.0/"
LASTFM_AUTH_REDIRECT = '/'
