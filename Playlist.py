import distance


class Playlist:
    def __init__(self, name):
        self.name = name
        self.track_list = []
        self.id = -1
        pass

    def add_track(self, album, artist, title):
        self.track_list.append(Track(album, artist, title))

    def __str__(self):
        return '{0} - {1} tracks'.format(self.name, len(self.track_list))

    def has_track(self, track_to_find):
        min_lev = 100
        for track in self.track_list:
            # name of songs can slightly change and still be in the playlist
            if track.title == track_to_find.title:
                return True
            sum_levenshtein = sum([distance.levenshtein(x, y) * z for x, y, z in
                                   [(track.artist, track_to_find.artist, 3),
                                    (track.title, track_to_find.title, 8)]])
            min_lev = min([sum_levenshtein, min_lev])

        if min_lev < 40:
            return True
        else:
            print('For {} - min_lev = {}'.format(track_to_find, min_lev))
            return False


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
