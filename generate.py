#!/usr/bin/env python
import os
import sys

import argparse

from subreddit_to_playlist import Subreddit, Playlist


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit",
        dest="subreddit",
        type=str,
        default="listentothis",
        help="Name of subreddit to grab songs from",
    )
    parser.add_argument(
        "--limit",
        dest="limit",
        type=str,
        default="week",
        help="How far back to search on Reddit, week/month etc.",
    )
    parser.add_argument(
        "--playlist-name",
        dest="playlist_name",
        type=str,
        default="'/r/listentothis' Top of this week",
        help="Name of playlist to create on Spotify",
    )
    parser.add_argument(
        "--username",
        dest="username",
        type=str,
        default="wilkinsss",
        help="Spotify user to create playlist for",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    reddit_client_id = os.environ["REDDIT_CLIENT_ID"]
    reddit_client_secret = os.environ["REDDIT_CLIENT_SECRET"]

    for key in [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "SPOTIPY_CLIENT_ID",
        "SPOTIPY_CLIENT_SECRET",
        "SPOTIPY_REDIRECT_URI",
    ]:
        if key not in os.environ:
            print("Please make sure env variables are set:\n-->", key, "is missing.")
            sys.exit(1)

    sub = Subreddit(args.limit, reddit_client_id, reddit_client_secret)
    posts = sub.get_posts_from(args.subreddit)

    playlist = Playlist(posts)
    playlist.update(args.playlist_name, args.username)


if __name__ == "__main__":
    main()
