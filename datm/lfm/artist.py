from api_base import APIObject, APIMeta, transformer


class Artist(APIObject):
    """A last.fm artist with the standard API calls."""

    __metaclass__ = APIMeta
    _methods_read = ['getCorrection', 'getEvents', 'getInfo', 'getPastEvents', 'getPodcast', 'getShouts',
                    'getSimilar', 'getTags', 'getTopAlbums', 'getTopFans', 'getTopTags', 'getTopTracks']
    _methods_write = ['addTags', 'removeTag', 'search', 'share', 'shout']

    @transformer
    def get_info(self, json_dict):
        pass