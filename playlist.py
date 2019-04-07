from funcy.seqs import first
import spotipy
import spotipy.util as util


class Playlist:
    def __init__(self, name, songs, scope):
        self.name = name
        self.songs = songs
        self.token_scope = scope
        self.spotify = None

    def create_for(self, username):
        print("Updating playlist with", len(self.songs), "songs")
        token = util.prompt_for_user_token(username, scope=self.token_scope)
        self.spotify = spotipy.Spotify(auth=token)

        fmt = u'artist:"{artist}" track:"{track}"'
        formatted_songs = (fmt.format(**song._asdict()) for song in self.songs)
        search_res = [
            self.spotify.search(q=s, type='track', limit=1)
            for s in formatted_songs
        ]
        track_ids = [(first(r.get('tracks', {}).get('items', {}))
                      or {}).get('uri') for r in search_res
                     if r.get('tracks', {}).get('items')]
        print("- Successfully found", len(track_ids),
              "songs, adding to playlist...")

        if token:
            self.spotify.trace = False
            playlists = self.spotify.user_playlists(username)
            playlist_id = [
                playlist['id'] for playlist in playlists['items']
                if playlist['name'] == self.name
            ]

            if playlist_id:
                self.spotify.user_playlist_replace_tracks(
                    username, playlist_id[0], track_ids)
                print("- Playlist generation successful")
            else:
                print("- Playlist doesn't exist")
        else:
            print("- Sorry, cannot get token for", username)
