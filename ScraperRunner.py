import configparser
import os

import sys
from gmusicapi import Mobileclient

import Playlist
import pymail


def dump_file(file, playlist_list):
    print('Dumping file')
    with open(file, 'w') as fwrite:
        for playlist in playlist_list:
            for track in playlist.track_list:
                fwrite.write(
                    '{0}{5}{1}{5}{2}{5}{3}{5}{4}'.format(playlist.name, track.album, track.artist, track.title, '\n',
                                                         Playlist.SEPARATOR))


def send_report_by_email(compare_report, email_address):
    print('Sending email')
    body = 'No track lost :)'
    nb_loss = len(compare_report)
    if nb_loss != 0:
        body = '\n'.join(compare_report)

    pymail.send_mail(body, '[GMPW]{} track(s) lost'.format(nb_loss), False, email_address)


def get_playlist_from_api(api):
    print('Connection OK. Retrieving playlist from google music')
    user_playlist = api.get_all_user_playlist_contents()
    print('{} playlist(s) found'.format(len(user_playlist)))
    playlist_list = []
    for playlist_with_content in user_playlist:
        cur_playlist = Playlist.Playlist(playlist_with_content['name'])
        cur_playlist.id = playlist_with_content['id']
        tracks_list = playlist_with_content['tracks']
        for track in tracks_list:
            if 'track' in track:
                real_track = track['track']
                cur_playlist.add_track(real_track['album'], real_track['artist'], real_track['title'])
        playlist_list.append(cur_playlist)
    print('Playlists retrieved')
    return playlist_list


def get_playlist_list_from_file(persisted_file):
    playlist_list = []
    cur_name = ''
    if os.path.exists(persisted_file):
        print('Get playlist from {0}'.format(persisted_file))
        splitted_lines = [x.strip().split(Playlist.SEPARATOR) for x in open(persisted_file, 'r')]
        for splitted_line in splitted_lines:
            if cur_name != splitted_line[0]:
                cur_name = splitted_line[0]
                cur_playlist = Playlist.Playlist(cur_name)
                playlist_list.append(cur_playlist)
            cur_playlist.add_track(splitted_line[1], splitted_line[2], splitted_line[3])
    else:
        print("File {0} doesn't exist".format(persisted_file))

    return playlist_list


def compare_playlist(playlist_list_from_api, playlist_list_from_file):
    print('Looking for missing element from api compared to file')
    report = []
    for playlist_api in playlist_list_from_api:
        print(f"Processing [{playlist_api.name}] playlist..")
        for playlist_file in playlist_list_from_file:
            if playlist_api.name == playlist_file.name:
                if set(playlist_api.track_list) != set(playlist_file.track_list):
                    for track in playlist_file.track_list:
                        if not playlist_api.has_track(track):
                            process_discrepancy(playlist_api, report, track)

    if len(report) == 0:
        print('No track lost or enough retrieved')
    return report


def process_discrepancy(playlist_api, report, track):
    message = "Playlist [{}]: missing\n{}".format(playlist_api.name, str.center(str(track), 130, " "))
    print(message)
    result = api.search("{} {}".format(track.title, track.artist))
    try:
        replacement_track = result['song_hits'][0]['track']
    except:
        replacement_track = None
    if replacement_track is None:
        report.append(message)
    else:
        artist = replacement_track["artist"]
        title = replacement_track["title"]
        answer = input("Wanna replace this missing song by:\n{}\nfound ?(Y/n)".format(
            str.center(f"{artist}-{title}", 130, " "))).lower()
        if answer != 'n':
            api.add_songs_to_playlist(playlist_api.id, replacement_track["storeId"])


config = configparser.ConfigParser()
if len(sys.argv) == 2:
    config_file = str(sys.argv[1]).replace('~', os.path.expanduser('~'))
else:
    config_file = os.path.join(os.path.expanduser("~"), 'Music/GmusicPlaylistScrapperConfig.ini')

print('Loading configuration from {0}'.format(config_file))
config.read(config_file)

google_credential = 'GmailAccountInfo'
if google_credential not in config:
    raise ValueError(f"Config file {config_file} doesn't contains {google_credential} tag")

api = Mobileclient()

email_address = config[google_credential]['gmailEmail']
email_pass = config[google_credential]['gmailAppPassword']
print('Connecting to gmusic api with {0}'.format(email_address))
logged_in = api.login(email_address, email_pass, Mobileclient.FROM_MAC_ADDRESS)

if not logged_in:
    raise ConnectionError('Unable to connect to address {0}'.format(email_address))

pymail.initialize(email_address, email_pass)

playlist_list_from_api = get_playlist_from_api(api)

persisted_file = os.path.normpath(os.path.expanduser(config['Persistence']['dumpFile']))
playlist_list_from_file = get_playlist_list_from_file(persisted_file)

compare_report = compare_playlist(playlist_list_from_api, playlist_list_from_file)

send_report_by_email(compare_report, [email_address])

dump_file(persisted_file, playlist_list_from_api)
