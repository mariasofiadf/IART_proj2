import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import sys

df_new = pd.read_csv('big_dataset.csv')
client_id = 'a07ad72e5f494ff793681e854bc90415'
client_secret = '6302d6b270c94cdf8ba4475367b48098'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

playlists = ['https://open.spotify.com/playlist/37i9dQZF1DWUZv12GM5cFk?si=1a5cf43c499547bc',  # Top Hits 2000
             'https://open.spotify.com/playlist/37i9dQZF1DX9Ol4tZWPH6V?si=6d30f1dd017f4ccf',  # Top Hits 2001
             'https://open.spotify.com/playlist/37i9dQZF1DX0P7PzzKwEKl?si=f4b48bfdefc74ad5',  # Top Hits 2002
             'https://open.spotify.com/playlist/37i9dQZF1DXaW8fzPh9b08?si=b224d7d239204609',  # Top Hits 2003
             'https://open.spotify.com/playlist/37i9dQZF1DWTWdbR13PQYH?si=03865913bc074f4b',  # Top Hits 2004
             'https://open.spotify.com/playlist/37i9dQZF1DWWzQTBs5BHX9?si=8d1f6eb9a9de45ed',  # Top Hits 2005
             'https://open.spotify.com/playlist/37i9dQZF1DX1vSJnMeoy3V?si=87213425e48c401a',  # Top Hits 2006
             'https://open.spotify.com/playlist/37i9dQZF1DX3j9EYdzv2N9?si=ddb1bf8e31fa48ce',  # Top Hits 2007
             'https://open.spotify.com/playlist/37i9dQZF1DWYuGZUE4XQXm?si=dd614b2027ee4e1c',  # Top Hits 2008
             'https://open.spotify.com/playlist/37i9dQZF1DX4UkKv8ED8jp?si=5d7436c6ff764429',  # Top Hits 2009
             'https://open.spotify.com/playlist/37i9dQZF1DXc6IFF23C9jj?si=3f8c3958edd14c8c',  # Top Hits 2010
             'https://open.spotify.com/playlist/37i9dQZF1DXcagnSNtrGuJ?si=9ae5898b67ab4f1b',  # Top Hits 2011
             'https://open.spotify.com/playlist/37i9dQZF1DX0yEZaMOXna3?si=bb469f7ef0824fb3',  # Top Hits 2012
             'https://open.spotify.com/playlist/37i9dQZF1DX3Sp0P28SIer?si=8bd8fc2055244f68',  # Top Hits 2013
             'https://open.spotify.com/playlist/37i9dQZF1DX0h0QnLkMBl4?si=aee3decb412640ea',  # Top Hits 2014
             'https://open.spotify.com/playlist/37i9dQZF1DX9ukdrXQLJGZ?si=819ceb23b9544e8f',  # Top Hits 2015
             'https://open.spotify.com/playlist/37i9dQZF1DX8XZ6AUo9R4R?si=2ddf60609ae84663',  # Top Hits 2016
             'https://open.spotify.com/playlist/37i9dQZF1DWTE7dVUebpUW?si=ced29738a5434f97',  # Top Hits 2017
             'https://open.spotify.com/playlist/37i9dQZF1DXe2bobNYDtW8?si=d336eea3e76d4e6a',  # Top Hits 2018
             'https://open.spotify.com/playlist/37i9dQZF1DWVRSukIED0e9?si=463c810dde86490a',  # Top Hits 2019
             'https://open.spotify.com/playlist/37i9dQZF1DX4o1oenSJRJd?si=41fbe1af37784c8b',  # All Out 2000's
             'https://open.spotify.com/playlist/37i9dQZF1DX5Ejj0EkURtP?si=766ac48f0c0a443a',  # All Out 2010's
             'https://open.spotify.com/playlist/1HvGDVJGq2iDKy7lFQ5tvx?si=63e0be1bf2834463',  # 10's Hits
             'https://open.spotify.com/playlist/37i9dQZF1DWWylYLMvjuRG?si=7fb0e6c489ce4e13',  # Party Hits 2010s
             'https://open.spotify.com/playlist/1U3x51O0LQ4TtaD5CgxuGL?si=15683fe640a44495',  # 00s HITS
             'https://open.spotify.com/playlist/37i9dQZF1DX7e8TjkFNKWH?si=826e194997b14d1b',  # Party Hits 2000s
             'https://open.spotify.com/playlist/37i9dQZF1DWUaThf8nMdW6?si=8ac8c39fec3b487c',  # Best of 'OOs Pop
             'https://open.spotify.com/playlist/14yNrYp9yYQYQukBAYYu3k?si=48a5fdeb32124d68',  # 10s pop gems
             'https://open.spotify.com/playlist/15sZyUgStYmvzm3QfdVDIp?si=05f36705f11e4319',  # 2000s-2010s bangers
             ]

playlists = list(set(playlists))  # Remove duplicate playlists

def add_playlist_to_dataset(df,playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    print("Adding playlist", sp.playlist(playlist_URI)["name"], "to dataset", )
    tracks = sp.playlist_tracks(playlist_URI)["items"]
    for track in tracks:
        # URI
        track_uri = track["track"]["uri"]
        # Track name
        song = track["track"]["name"]

        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # Name, popularity, genre
        artist = track["track"]["artists"][0]["name"]
        explicit = track["track"]["explicit"]
        year = track["track"]["album"]["release_date"][:4]
        popularity = track["track"]["popularity"]

        feats = sp.audio_features(track_uri)[0]
        if feats is None:
            continue
        duration_ms = feats.get("duration_ms")
        danceability = feats.get("danceability")
        energy = feats.get("energy")
        key = feats.get("key")
        loudness = feats.get("loudness")
        mode = feats.get("mode")
        speechiness = feats.get("speechiness")
        acousticness = feats.get("acousticness")
        instrumentalness = feats.get("instrumentalness")
        liveness = feats.get("liveness")
        valence = feats.get("valence")
        tempo = feats.get("tempo")
        if len(artist_info["genres"]) < 1:
            genre = ""
        else:
            genre = artist_info["genres"][0]

        row = [artist,song,duration_ms,explicit,year,popularity,
               danceability, energy, key, loudness, mode, speechiness,
               acousticness, instrumentalness, liveness, valence, tempo, genre]
        df_row = pd.DataFrame([row], columns=df.columns.values)

        df = pd.concat([df, df_row])

    return df


def add_album_to_dataset(df,album_id):
    tracks = sp.album_tracks(album_id=album_id)["items"]
    album = sp.album(album_id=album_id)
    for track in tracks:
        # URI
        track_uri = track["uri"]
        # Track name
        song = track["name"]

        # Main Artist
        artist_uri = track["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # Name, popularity, genre
        artist = track["artists"][0]["name"]
        explicit = track["explicit"]
        year = album["release_date"][:4]
        popularity = album["popularity"]

        feats = sp.audio_features(track_uri)[0]
        if feats is None:
            continue
        duration_ms = feats.get("duration_ms")
        danceability = feats.get("danceability")
        energy = feats.get("energy")
        key = feats.get("key")
        loudness = feats.get("loudness")
        mode = feats.get("mode")
        speechiness = feats.get("speechiness")
        acousticness = feats.get("acousticness")
        instrumentalness = feats.get("instrumentalness")
        liveness = feats.get("liveness")
        valence = feats.get("valence")
        tempo = feats.get("tempo")
        if len(artist_info["genres"]) < 1:
            genre = ""
        else:
            genre = artist_info["genres"][0]

        row = [artist,song,duration_ms,explicit,year,popularity,
               danceability, energy, key, loudness, mode, speechiness,
               acousticness, instrumentalness, liveness, valence, tempo, genre]
        df_row = pd.DataFrame([row], columns=df.columns.values)

        df = pd.concat([df, df_row])

    return df


def add_from_year(df, year, no_tracks):
    offset = 0
    start_size = df.shape[0]
    while offset < no_tracks:
        tracks = sp.search(q='year:' + str(year), limit=50, offset=offset)
        tracks = tracks["tracks"]
        for album in tracks["items"]:
            album_url = album["album"]["id"]
            print(album["name"])
            df = add_album_to_dataset(df, album_url)
            count = df.shape[0]-start_size
            print("count:", count)
            if count > no_tracks:
                df.drop_duplicates()
                return df
        offset += 50
    df.drop_duplicates()
    return df


start_year = 2020
end_year = 2022
print("extracting from ", start_year, "to", end_year)
for year in range(start_year, end_year):
    print("Adding from year", year)
    name = "new_data_2020_2021" + str(year)
    if year == 2021:
        df_new = add_from_year(df_new, year, 500)
    else:
        df_new = add_from_year(df_new, year, 1000)

    df_new.to_csv(name, index=False)

# for i, playlist in enumerate(playlists):
#     print(i/len(playlists)*100, "%")
#     df_new = add_playlist_to_dataset(df_new, playlist)

# df_new.drop_duplicates()
# print("New dataset shape: ", df_new.shape)
# print("Saved to file new_data_albums.csv")
# df_new.to_csv('new_data_playlists.csv', index=False)

