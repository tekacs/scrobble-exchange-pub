"""A simple harness to test datm.lfm from the REPL"""

import webbrowser
from datm.lfm import RequestBuilder, Artist, User, Auth

API_KEY = '<KEY>'
API_SECRET = '<SECRET>'
rb = RequestBuilder(API_KEY, API_SECRET, '<USERNAME>')
coldplay = Artist.get_info(rb.params(artist='Coldplay', autocorrect=1), _debug=True)
similar = Artist.get_similar(rb.params(artist='Coldplay', autocorrect=1), _debug=True)
token = Auth.get_token(rb.auth(rb.params()), _debug=True)
webbrowser.open('http://www.last.fm/api/auth?api_key=%s&token=%s' % (API_KEY, token))
raw_input('Press <ENTER> after granting access...')
session = Auth.get_session(rb.auth(rb.params(token=token)), _debug=True)