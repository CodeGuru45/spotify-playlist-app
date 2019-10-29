import spotipy
import spotipy.util as util
import dateutil.parser as dp
import datetime
import pickle
import os.path
from os import path

cid ="ab918d7eb7af4300bb0fb9c015655705" 
secret = "07f70730548c46a09880d38c1d375271"
username = "musicguru45"
scope = "playlist-modify-public playlist-modify-private user-library-read playlist-read-private"
token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri="http://localhost:8888/")

if token:
    sp = spotipy.Spotify(auth=token)

    def get_song_ids(user, playlist_id):
        ids = []
        playlist = sp.user_playlist(user, playlist_id)
        tracks = playlist["tracks"]
        if tracks["items"]:
            for item in tracks["items"]:
                track = item["track"]
                ids.append(track["id"])

        return ids

    def update(user, liked_songs, playlist_id):
        song_ids = get_song_ids(user, playlist_id)
        curr_date = datetime.datetime.now()
        curr_day = curr_date.day
        track_ids = []
        for item in liked_songs["items"]:
            date = item["added_at"]
            datetime_obj = dp.parse(date)
            elapsed = curr_day - datetime_obj.day
            if abs(elapsed) <= 5:
                track = item["track"]
                if (track["id"] in song_ids) == False:
                    track_ids.append(track["id"])

        sp.user_playlist_add_tracks(username, playlist_id, track_ids)   

    if path.exists("playlist_id.pckl") == False:
        res = input("Enter number of days to download songs within: ")
        playlist_name = "Recently Added"
        sp.user_playlist_create(username, playlist_name)
        playlists = sp.current_user_playlists()
        new_playlist = playlists["items"][0]
        new_playlist_id = new_playlist["id"]
        results = sp.current_user_saved_tracks(limit=50)
        update(username, results, new_playlist_id)
        f = open('playlist_id.pckl', 'wb')
        pickle.dump(new_playlist_id, f)
        f.close()
    
    else:
        f = open('playlist_id.pckl', 'rb')
        playlist_id = pickle.load(f)
        f.close()
        
        results = sp.current_user_saved_tracks(limit=50)
        update(username, results, playlist_id) 
 
else:
    print("Can't get token for", username)



  