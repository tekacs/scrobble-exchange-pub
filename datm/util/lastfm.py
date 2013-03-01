"""These utilities try to bridge the gap between lfm and DATM.

The lfm library is quite nice (if I do say so myself) but uses a somewhat
different style to DATM (it's procedural like the last.fm API rather than
object-oriented).

I've also kept lfm pretty pure and free from the concerns of practicality, by
and large. The seeming hacks herein should make the syntax rather less verbose
and arcane for practical queries, though. :P
"""

__author__ = 'amar'

def params(config, dictargs=(), **kwargs):
    kwargs.update(dictargs)
    return config.lastfm.rb.params(kwargs)

def auth_params(config, dictargs=(), **kwargs):
    kwargs.update(dictargs)
    return config.lastfm.rb.auth(params(config, kwargs))