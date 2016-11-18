class Playlist:
    def __init__(self, name):
        self.name = name
        self.track_list = []
        pass

    def add_track(self, album, artist, title):
        self.track_list.append(Track(album, artist, title))

    def __str__(self):
        return '{0} - {1} tracks'.format(self.name, len(self.track_list))

    def has_track(self, track_to_find):
        return track_to_find in self.track_list


SEPARATOR = ';'


class Track:
    def __init__(self, album, artist, title):
        self.album = album.replace(SEPARATOR, '')
        self.artist = artist.replace(SEPARATOR, '')
        self.title = title.replace(SEPARATOR, '')

    def __key(self):
        return (self.album, self.artist, self.title)

    def __eq__(self, y):
        return self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.title, self.artist, self.album)
