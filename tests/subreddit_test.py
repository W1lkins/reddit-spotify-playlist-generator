import unittest
from collections import namedtuple

from subreddit_to_playlist.subreddit import Subreddit


class SubredditTest(unittest.TestCase):
    def test_update_title(self):
        subreddit = Subreddit(1, 'foo', 'bar')
        track = namedtuple('track', ['artist', 'track'])

        # test valid format
        title = subreddit._update_title('foo -- bar [baz] (2019)')
        self.assertEqual(title, track(artist='foo', track='bar'))

        # test ValueException when not enough values to unpack
        title = subreddit._update_title('foo')
        self.assertEqual(title, None)

        # test only splits once
        title = subreddit._update_title('foo -- bar -- baz')
        self.assertEqual(title, track(artist='foo', track='bar -- baz'))
