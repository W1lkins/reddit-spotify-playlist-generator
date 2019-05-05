import unittest
from collections import namedtuple

from subreddit_to_playlist.playlist import Playlist


class PlaylistTest(unittest.TestCase):
    def test_format_songs(self):
        track = namedtuple('track', ['artist', 'track'])

        songs = [track('foo', 'bar')]
        playlist = Playlist(songs)

        self.assertEqual(next(playlist._format_songs()), "artist:'foo' track:'bar'")

    def test_generate_track_ids(self):
        results = [
            {'tracks': {'items': [{'uri': 'spotify:track:foo'}]}}
        ]

        playlist = Playlist([])
        ids = playlist._generate_track_ids(results)

        self.assertEqual(ids, ['spotify:track:foo'])
