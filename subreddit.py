from collections import namedtuple
import praw
import re


class Subreddit:
    def __init__(self, name, limit, agent, client_id, client_secret):
        self.name = name
        self.limit = limit
        self.reddit = praw.Reddit(
            user_agent=agent, client_id=client_id, client_secret=client_secret)
        self.track = namedtuple('track', ['artist', 'track'])

    def get_posts(self):
        return [
            self.fix_title(post.title)
            for post in list(self.reddit.subreddit(self.name).top(self.limit))
            if self.fix_title(post.title)
        ]

    def fix_title(self, song_title):
        try:
            artist, title = re.split(' -+ ', song_title, 1)
        except ValueError:
            print("Got value error for song", song_title)
            return None
        return self.track(artist.strip(), title.partition('[')[0].strip())
