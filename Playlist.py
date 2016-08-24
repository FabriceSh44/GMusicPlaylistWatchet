class Playlist():
    def __init__(self, name):
        self.name = name
        self.track_list = []
        pass

    def add_track(self, album, artist, title):
        self.track_list.append((album, artist, title))

    def __str__(self):
        return '{0} - {1} tracks'.format(self.name, len(self.track_list))

    def has_track(self, track_to_find):
        for track in self.track_list:
            if track[0] == track_to_find[0] and track[1] == track_to_find[1] and track[2] == track_to_find[2]:
                return True
        return False

