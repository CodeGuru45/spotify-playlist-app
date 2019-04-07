import spotipy
import spotipy.util as util
import dateutil.parser as dp
import datetime

cid ="ab918d7eb7af4300bb0fb9c015655705" 
secret = "07f70730548c46a09880d38c1d375271"
username = "musicguru45"
scope = "playlist-modify-public playlist-modify-private user-library-read playlist-read-private"
token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri="http://localhost:8888/")

if token:
    sp = spotipy.Spotify(auth=token)
    bound = input("Add songs downloaded within the last how many days: ")
    playlist_name = "Saved Within Last " + str(bound) + " Days"
    curr_date = datetime.datetime.now()
    curr_day = curr_date.day
    sp.user_playlist_create(username, playlist_name)
    playlists = sp.current_user_playlists(limit=50, offset=0)
    new_playlist = playlists["items"][0]
    new_playlist_id = new_playlist["id"]
    track_ids = []
    users_saved_tracks = sp.current_user_saved_tracks(limit=50, offset=0)
    for item in users_saved_tracks["items"]:
        date = item["added_at"]
        datetime_obj = dp.parse(date)
        elapsed = curr_day - datetime_obj.day
        if abs(elapsed) <= int(bound):
            track = item["track"]
            track_ids.append(track["id"])   
  
    sp.user_playlist_add_tracks(username, new_playlist_id, track_ids) 

else:
    print("Can't get token for", username)
