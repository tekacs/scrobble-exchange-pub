import functools

__author__ = 'amar'

def memoised_property(f):
    name = '__mem_%s' % f.__name__
    # N.B. This won't be name-mangled, but nobody uses double-underscored names
    #      anyway (and you can't even *define* them from within a class without
    #      using setattr directly! :P)
    @property
    @functools.wraps(f)
    def wrapper(self):
        v = getattr(self, name, None)
        if v is None:
            v = f(self)
            setattr(self, name, v)
        return v
    return wrapper