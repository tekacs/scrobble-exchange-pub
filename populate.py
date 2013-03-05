#!/usr/bin/env python
"""Populate the database with some test data!"""
import uuid
import random

import datm
import datm.models
from datm.util import db, magic
import mechanics

config = datm.DATMConfig(
    db_args={
        'url': 'sqlite:///db',
        'pool_size': None,
        'max_overflow': None,
        'echo': True
    },
    lastfm={
        'api_key': 'c5e4c807a729d051943be6859902e430',
        'api_secret': '3a2d5e8514ec53cc230fd7095df54003'
    }
)

session = datm.DATMSession(config)
config = session.bind()

config.db.create_all()

league_data = (
    ('op', 'Operator', 'icon-beaker#040404', 'Dial 100 for broken pipe'),
    ('gold', 'Gold', 'icon-circle#FFD700', 'Shiny!'),
    ('silver', 'Silver', 'icon-circle#C0C0C0', 'Antibacterial!'),
    ('bronze', 'Bronze', 'icon-circle#CD7F32', 'Tarnished!')
)

trophy_data = (
    ('medal', 'Medal', 'icon-time#FFD700', 'Here, have a medal!'),
    ('harry-potter', 'Harry Potter', 'icon-bolt#040404', 'The One Who Lived'),
    ('lemon', 'Lemon', 'icon-lemon#FCF141', 'Lemony goodness!'),
    ('over9k', '9001', 'icon-chevron-up#040404', 'It\'s Over 9000!')
)

op_data = (
    'tekacs',
    'joebateson',
    'Sov1etRuss1a',
    'neilsatra'
)

lastfm_data = (
    'simonmoran',
    'foreverautumn',
    'theneonfever',
    'robinlisle',
    'nancyvw',
    'miadellocca',
    'massdosage',
    'mbrodbelt',
    'hyperchris01',
    'ben-xo',
    'gamboviol',
    'good_bone',
    'caitlin',
    'francescatanner',
    'Knapster01',
    'eartle',
    'teabot',
    'jorge',
    'colins',
    'sjransome',
    'Maddieman',
    'wsbk',
    'darkspark88',
    'grahamtodman',
    'y0b1tch',
    'monkeyhacker',
    'FofR',
    'Pbad',
    'pellitero',
    'dasistdasende',
    'Thomas_prince',
    'sven',
    'CarbonParlour',
    'phuedx',
    'tdhooper',
    'pduin',
    'ssk2',
    'marekventur',
    'jammus',
    'dodgyfox',
    'okspud1'
)

def random_colour():
    return ''.join(hex(random.randrange(256))[2:].zfill(2) for _ in range(3))

leagues = []
trophies = []
users = []

auth = datm.Auth(config)
auth.create(secret=str(uuid.uuid4()))

for d in league_data:
    l = datm.League(config, uid=d[0])
    if not l.persisted:
        l = datm.League(config, uid=d[0], name=d[1], icon=d[2], description=d[3])
        l.create()
    leagues.append(l)

for d in trophy_data:
    t = datm.Trophy(config, uid=d[0])
    if not t.persisted:
        t = datm.Trophy(config, uid=d[0], name=d[1], icon=d[2], description=d[3])
        t.create()
    trophies.append(t)

op = datm.League(config, 'op')
over9k = datm.Trophy(config, 'over9k')
for name in op_data:
    u = datm.User(config, name)
    if not u.persisted:
        u.create(money=10**6, points=9001, league=op)
        u.add_trophy(over9k)
    users.append(u)

bronze = datm.League(config, 'bronze')
for name in lastfm_data:
    u = datm.User(config, name)
    if not u.persisted:
        u.create(money=20000, points=0, league=bronze)
    users.append(u)

output = []
for u in users:
    for a in u.top_artists(limit=10):
        if a.mbid == '':
            output.append((a.name, a.mbid))
            continue
        m = mechanics.Artist(a)
        if not a.persisted:
            a.create(price=m.initial_price, max_available=m.max_shares)
        if not u.owns(a):
            try:
                mechanics.User(u).buy(a, m.price(owned=False))
            except mechanics.NotEnoughMoneyError as e:
                output.append(e)
            except mechanics.NoStockRemainingException as e:
                output.append(e)

db.commit(config)

print '\n'.join(str(o) for o in output)
print 'No. errors:', len(output)
