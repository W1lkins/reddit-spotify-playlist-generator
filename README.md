# reddit-spotify-playlist-generator 🎵

A simple way to generate a Spotify playlist based on posts from a specific
Subreddit.

Uses praw for interacting with the Reddit API and Spotipy to interact with the
Spotify API.

You'll need a developer app on Reddit which can be created
[here](https://www.reddit.com/prefs/apps/). You'll also need a developer app on
Spotify which can be created
[here](https://developer.spotify.com/dashboard/applications).

**Table of Contents**

<!-- toc -->

- [Installation](#installation)
    + [Running with Docker](#running-with-docker)
- [Usage](#usage)
- [Development](#development)

<!-- tocstop -->

## Installation

#### Running with Docker

```console
$ docker run -it --rm \
    -e REDDIT_CLIENT_ID=<reddit-client-id> \
    -e REDDIT_CLIENT_SECRET=<reddit-client-secret> \
    -e SPOTIPY_CLIENT_ID=<spotify-client-id> \
    -e SPOTIPY_CLIENT_SECRET=<spotify-client-secret> \
    -e SPOTIPY_REDIRECT_URI=<local-callback-uri> \
    w1lkins/reddit-to-spotify
```

## Usage

```console
usage: generate.py [-h] [--subreddit SUBREDDIT] [--limit LIMIT]
                   [--playlist-name PLAYLIST_NAME] [--username USERNAME]

optional arguments:
  -h, --help            show this help message and exit
  --subreddit SUBREDDIT
                        Name of subreddit to grab songs from
  --limit LIMIT         How far back to search on Reddit, week/month etc.
  --playlist-name PLAYLIST_NAME
                        Name of playlist to create on Spotify
  --username USERNAME   Spotify user to create playlist for
```

## Development

You'll need all the aforementioned environment variables exported within your
environment:

```console
REDDIT_CLIENT_ID=<reddit-client-id>
REDDIT_CLIENT_SECRET=<reddit-client-secret>
SPOTIPY_CLIENT_ID=<spotify-client-id>
SPOTIPY_CLIENT_SECRET=<spotify-client-secret>
SPOTIPY_REDIRECT_URI=<local-callback-uri>
```

Then, ensure python3+ is installed and run `make virtual`.

Next, run `source venv/bin/activate` then `make install` to install the libraries in `requirements.txt`.

You should now be able to run `make` which will run `./generate.py`
