from interfaces.spotify_api import *
from interfaces.youtube_api import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

#

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/spotify_api')
async def spotify_api():
    sp = Spotify()
    playlists = sp.get_user_playlists_list()
    playlists_with_tracks = sp.get_tracks_from_playlists(playlists[:3])
    return playlists_with_tracks  ## return playlists dict with playlist_id,_name,tracks


@app.post('/youtube_api')
async def youtube_api(playlists: list[dict]):
    youtube = Youtube()
    for playlist in playlists:
        playlist_id = youtube.get_playlist_youtube_id(
            playlist['playlist_name'])  ##creates playlist with given name & returns its id
        for track in playlist['tracks'][:5]:
            if track["isSelected"]:
                video_id = youtube.get_track_youtube_id(track["track_name"])
                youtube.add_track_to_playlist(playlist_id, video_id)
    return "Playlists Created"
