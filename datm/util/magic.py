import threading
import functools

__author__ = 'amar'

def memoised_property(f):
    """Create a (writable) property which serves up memoised data or calculates
    it if it is not already stored.

    Memoisation lasts for the duration of the class instance's existence.

    Setting and deleting values writes directly to the memoised store to allow
    for pre/external-calculation to be performed and the value set in such a
    fashion and to allow for forced recalculation (just ``del`` the attribute!)
    """
    # FIXME: This is currently NOT THREADSAFE (due to None recur fix). Lock!
    name = '_{}'.format(f.__name__)
    @property
    @functools.wraps(f)
    def wrapper(self):
        try:
            v = getattr(self, name)
        except AttributeError:
            setattr(self, name, None)
            try:
                v = f(self)
            finally:
                delattr(self, name)
            setattr(self, name, v)
        return v

    @wrapper.setter
    def wrapper(self, v):
        setattr(self, name, v)

    @wrapper.deleter
    def wrapper(self):
        delattr(self, name)
    return wrapper

def underscore_property(name):
    """Create a property which gets to/from an underscore variable on self.

    These are used to ensure that property semantics are used whilst allowing
    for future replacement with actual properties.

    What's the advantage of doing this over using straight attributes?
    Quite apart from the persistent attribute, and avoidance of accidentally
    setting class attributes, properties have a few quirks. :/

    This also provides a really handy placeholder to indicate that something
    may/should be replaced in future with a more manipulative property.
    """
    name = '_{}'.format(name)
    @property
    def prop(self):
        return getattr(self, name)
    @prop.setter
    def prop(self, value):
        setattr(self, name, value)
    @prop.deleter
    def prop(self):
        delattr(self, name)
    return prop

class PartialDict(dict):
    def __init__(self, partial_dict, populator):
        self.update(partial_dict)
        self.populator = populator
        self.direct_get = super(PartialDict, self).__getitem__
        self.full = False

    def __getitem__(self, item):
        if not self.full:
            if not item in self.keys():
                self.update(self.populator())
        return self.direct_get(item)