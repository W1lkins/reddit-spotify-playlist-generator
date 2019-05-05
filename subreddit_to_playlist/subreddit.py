from collections import namedtuple
import praw
import re


class Subreddit:
    def __init__(self, limit, client_id, client_secret):
        self.limit = limit
        self.reddit_instance = praw.Reddit(
            user_agent="spotify playlist generator",
            client_id=client_id,
            client_secret=client_secret,
        )
        self.title_format = namedtuple("track", ["artist", "track"])

    def get_posts_from(self, name):
        return [
            self._update_title(post.title)
            for post in list(self.reddit_instance.subreddit(name).top(self.limit))
            if self._update_title(post.title)
        ]

    def _update_title(self, song_title):
        try:
            artist, title = re.split(" -+ ", song_title, 1)
        except ValueError:
            return None
        return self.title_format(artist.strip(), title.partition("[")[0].strip())
