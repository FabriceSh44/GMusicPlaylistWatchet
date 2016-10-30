class Playlist():
    def __init__(self, name):
        self.name = name
        self.track_list = []
        pass

    def add_track(self, album, artist, title):
        self.track_list.append(Track(album, artist, title))

    def __str__(self):
        return '{0} - {1} tracks'.format(self.name, len(self.track_list))

    def has_track(self, track_to_find):
        for track in self.track_list:
            if track.album == track_to_find.album and track.artist == track_to_find.artist and track.title == track_to_find.title:
                return True
        return False


class Track():
    def __init__(self, album, artist, title):
        self.album = album
        self.artist = artist
        self.title = title
