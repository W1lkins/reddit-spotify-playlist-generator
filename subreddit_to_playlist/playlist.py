from funcy.seqs import first
from loguru import logger
from tqdm import tqdm
import spotipy
import spotipy.util as util
import sys


class Playlist:
    def __init__(self, songs):
        self.songs = songs
        self.spotify = None

    def _get_spotify_instance(self, username):
        token = util.prompt_for_user_token(username,
                                           scope="playlist-modify-public")
        if not token:
            logger.critical("could not get token for user")
            sys.exit(1)

        self.spotify = spotipy.Spotify(auth=token)

    def _format_songs(self):
        fmt = u"artist:'{artist}' track:'{track}'"
        return (fmt.format(**song._asdict()) for song in self.songs)

    def _generate_track_ids(self, results):
        return [(first(r.get("tracks", {}).get("items", {})) or {}).get("uri")
                for r in results if r.get("tracks", {}).get("items")]

    def create(self, playlist_name, username):
        return self.spotify.user_playlist_create(username, playlist_name)

    def update(self, playlist_name, username):
        self._get_spotify_instance(username)

        logger.info("searching for %d songs on spotify" % len(self.songs))
        search_res = [
            self.spotify.search(q=s, type="track", limit=1) for s in tqdm(
                self._format_songs(), unit=" songs", total=len(self.songs))
        ]
        track_ids = self._generate_track_ids(search_res)
        logger.info("found %d actual songs" % len(track_ids))
        logger.info("attempting to add songs to playlist")

        self.spotify.trace = False
        playlists = self.spotify.user_playlists(username)
        playlist_ids = [
            playlist["id"] for playlist in playlists["items"]
            if playlist["name"] == playlist_name
        ]

        if playlist_ids:
            playlist_id = playlist_ids[0]
        else:
            logger.info("playlist does not already exist, creating")
            playlist = self.create(playlist_name, username)
            playlist_id = playlist["id"]

        if not playlist_id:
            logger.critical("could not create playlist")
            sys.exit(1)

        logger.info("replacing tracks in playlist")
        self.spotify.user_playlist_replace_tracks(username, playlist_id,
                                                  track_ids)
        logger.info("playlist generation successful")
