import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd


def get_track_features(sp, track_id):
    track_features = sp.audio_features(track_id)

    if track_features:
        return track_features[0]  # Return the first element of the list
    else:
        return None


def get_top_track(sp, artist_id):
    top_tracks = sp(artist_id)

    if top_tracks and "tracks" in top_tracks:
        tracks = top_tracks["tracks"]
        if tracks:
            top_track = tracks[0]
            track_name = top_track["name"]
            album = top_track["album"]["name"]
            track_url = top_track["external_urls"]["spotify"]
            preview_url = top_track["preview_url"]
            return {
                "Track_Name": track_name,
                "Album": album,
                "Track_URL": track_url,
                "Preview_URL": preview_url,
            }

    return None


# Set up authentication with Spotipy
sp_auth = SpotifyOAuth(
    client_id='b950e05abe284cd99ab06198889b4d89',
    client_secret='8b5f63713f8546798776aa955db7feb4',
    redirect_uri='http://localhost:3000/callback',
    scope='user-read-recently-played, user-top-read'
)

# Auth step
try:
    token_info = sp_auth.get_cached_token()
    if not token_info:
        token_info = sp_auth.get_access_token()
except spotipy.SpotifyOAuthError as e:
    print("Error during authentication:", e)
    token_info = None

if token_info:
    # Create Spotify object
    sp = spotipy.Spotify(auth=token_info['access_token'])

    try:

        # declare time ranges
        time_ranges = ['short_term', 'medium_term', 'long_term']

        # Get my recently played tracks 50
        recent_played_tracks = sp.current_user_recently_played(limit=50)

        recent_played_tracks_data = []
        for track in recent_played_tracks['items']:

            track_id = track["track"]["id"]
            track_features = get_track_features(sp, track_id)

            if track_features:
                danceability = track_features["danceability"]
                energy = track_features["energy"]
                speechiness = track_features["speechiness"]
                acousticness = track_features["acousticness"]
                instrumentalness = track_features["instrumentalness"]
                liveness = track_features["liveness"]
                valence = track_features["valence"]
                tempo = track_features["tempo"]

            track_info = {
                'Track Name': track['track']['name'],
                'Artist Name': track['track']['artists'][0]['name'],
                'Album Name': track['track']['album']['name'],
                'Played At': track['played_at'],
                'Duration (ms)': track['track']['duration_ms'],
                'Popularity':  track["track"]["popularity"],
                "Danceability": danceability,
                "Energy": energy,
                "Speechiness": speechiness,
                "Acousticness": acousticness,
                "Instrumentalness": instrumentalness,
                "Liveness": liveness,
                "Valence": valence,
                "Tempo": tempo,
            }

            recent_played_tracks_data.append(track_info)

        # Get my top artists in all the time ranges
        top_artists_data = []
        for time_range in time_ranges:
            top_artists = sp.current_user_top_artists(
                limit=50, time_range=time_range)

            for artist in top_artists['items']:
                artist_info = {
                    'Artist Name': artist['name'],
                    'Genres': ', '.join(artist['genres']),
                    'Popularity': artist['popularity'],
                    'Followers': artist['followers']['total'],
                    'Image URL': artist['images'][0]['url'] if artist['images'] else None,
                    'Time Range': time_range,
                }
                top_artists_data.append(artist_info)

        # Get my top tracks in all the time ranges
        top_tracks_data = []
        for time_range in time_ranges:
            top_tracks = sp.current_user_top_tracks(
                limit=50, time_range=time_range)

            for track in top_tracks['items']:
                artist_id = track['artists'][0]['id']

                # Get track details including genres
                artist_details = sp.artist(track['artists'][0]['id'])
                genres = ', '.join(artist_details['genres'])

                track_info = {
                    'Track Name': track['name'],
                    'Artist Name': track['artists'][0]['name'],
                    'Album Name': track['album']['name'],
                    'Popularity': track['popularity'],
                    'Time Range': time_range,
                    'Genres': genres
                }
                top_tracks_data.append(track_info)

    except spotipy.SpotifyException as e:
        print("Error retrieving data:", e)

    # Save the data into separate sheets of an Excel file
    with pd.ExcelWriter('New_MY_SpotifyData.xlsx') as writer:
        recent_played_df = pd.DataFrame(recent_played_tracks_data)
        top_artists_df = pd.DataFrame(top_artists_data)
        top_tracks_df = pd.DataFrame(top_tracks_data)

        recent_played_df.to_excel(
            writer, sheet_name='Recently_Played', index=False)
        top_artists_df.to_excel(writer, sheet_name='Top_Artists', index=False)
        top_tracks_df.to_excel(writer, sheet_name='Top_Tracks', index=False)

    print("Data saved to Excel: New_MY_SpotifyData.xlsx")

else:
    print("*****Authentication failed*****")
