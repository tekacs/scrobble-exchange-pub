"""A demonstration of how DATM should be imported and configured."""

# At startup time for your long-running server:

import datm
import my_config

lastfm_config = {
    'api_key': my_config.lastfm['api_key'],
    'secret': my_config.lastfm['secret']
}

db_args = {
    'url': 'sqlite:///:memory:'
}

config = datm.DATMConfig(lastfm=lastfm_config, db_args=db_args)

...

# Then in each local context (say serving thread, analytics callback):

with datm.DATMSession(config): # this will be stored in threading.local
    ... # and here goes your code
