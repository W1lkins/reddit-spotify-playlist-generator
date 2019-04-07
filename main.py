#!/usr/bin/env python
import click
import os
import sys

from subreddit import Subreddit
from playlist import Playlist

scope = 'playlist-modify-public'
user_agent = 'listentothis playlist generator'
reddit_client_id = os.environ["REDDIT_CLIENT_ID"]
reddit_client_secret = os.environ["REDDIT_CLIENT_SECRET"]

for key in [
        "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "SPOTIPY_CLIENT_ID",
        "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI"
]:
    if key not in os.environ:
        print("Please make sure env variables are set:\n-->", key,
              "is missing.")
        sys.exit(1)

#@click.command()
#@click.option('--subreddit', default='listentothis', help='Subreddit to get tracks from')
#@click.option('--limit', default='week', help='Usage "week","month","all"..', type=str)
sub = Subreddit(subreddit, limit, user_agent, reddit_client_id,
                reddit_client_secret)
posts = sub.get_posts()

#@click.command()
#@click.option('--playlist_name', default='"/r/listentothis" Top of this week', help='Playlist name')
playlist = Playlist(playlist_name, posts, scope)

#@click.command()
#@click.option('--username', help='Spotify username', prompt='Enter your Spotify username', type=str)
playlist.create_for(username)
