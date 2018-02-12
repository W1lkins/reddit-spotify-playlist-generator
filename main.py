#!/usr/bin/env python
from collections import namedtuple
from funcy.seqs import first
import click
import os
import praw
import re
import spotipy
import spotipy.util as util
import sys
import time

scope = 'playlist-modify-public'
user_agent = 'listentothis playlist generator'
reddit_client_id = os.environ["REDDIT_CLIENT_ID"]
reddit_client_secret = os.environ["REDDIT_CLIENT_SECRET"]
track = namedtuple('track', ['artist', 'track'])

def check_environment():
    for key in ["REDDIT_CLIENT_ID","REDDIT_CLIENT_SECRET","SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET","SPOTIPY_REDIRECT_URI"]:
        if key not in os.environ:
            print("Please make sure env variables are set:\n-->", key, "is missing.")
            sys.exit(1)

def attempt_fix_title(song_title):
  try:
    artist, title = re.split(' -+ ', song_title, 1)
  except ValueError:
    return None
  return track(artist.strip(), title.partition('[')[0].strip())

def get_songs_from_subreddit(subreddit, limit):
    r = praw.Reddit(
        user_agent=user_agent,
        client_id=reddit_client_id,
        client_secret=reddit_client_secret,
    )
    subreddit_posts = list(r.subreddit(subreddit).top(limit))
    return [attempt_fix_title(x.title) for x in subreddit_posts if attempt_fix_title(x.title)]

def create_spotify_playlist(songs, playlist_name, username):
    print("- Attempting to update playlist with", len(songs), "songs")
    token = util.prompt_for_user_token(username, scope=scope)
    spotify = spotipy.Spotify(auth=token)
    
    fmt = u'artist:"{artist}" track:"{track}"'
    formatted_songs = (fmt.format(**song._asdict()) for song in songs)
    search_res = [spotify.search(q=s, type='track', limit=1) for s in formatted_songs]
    track_ids = [(first(r.get('tracks', {}).get('items', {})) or {}).get('uri')
                        for r in search_res if r.get('tracks', {}).get('items')]
    print("- Successfully found", len(track_ids), "songs, adding to playlist...")

    if token:
        spotify.trace = False
        playlists = spotify.user_playlists(username)
        playlist_id = [playlist['id'] for playlist in playlists['items'] if playlist['name'] == playlist_name]

        if playlist_id:
            spotify.user_playlist_replace_tracks(username, playlist_id[0], track_ids)
            print("- Playlist generation successful")
        else:
            print("- Playlist doesn't exist")
    else:
        print("- Sorry, cannot get token for", username)

@click.command()
@click.option('--subreddit', default='listentothis', help='Subreddit to get tracks from')
@click.option('--limit', default='week', help='Usage "week","month","all"..', type=str)
@click.option('--username', help='Spotify username', prompt='Enter your Spotify username', type=str)
@click.option('--playlist_name', default='"/r/listentothis" Top of this week', help='Playlist name')

def subreddit_songs_to_playlist(subreddit, limit, username, playlist_name):
    create_spotify_playlist(get_songs_from_subreddit(subreddit, limit), playlist_name, username)

if __name__ == '__main__':
    check_environment()
    subreddit_songs_to_playlist()
