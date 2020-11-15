from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from os import path
from os import chdir

file_path = path.abspath(__file__)  # full path of the script
dir_path = path.dirname(file_path)  # full path of the directory of your script
chdir(dir_path)


class Youtube:
    def __init__(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube.force-ssl']
        )
        flow.redirect_uri="https://spoty-tube-api.herokuapp.com/"
        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials
        self.youtube = build("youtube", "v3", credentials=credentials)

    def get_track_youtube_id(self, track_name):
        request = self.youtube.search().list(
            part="snippet", q=track_name, maxResults=1
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        return video_id

    def get_playlist_youtube_id(self, playlist_name):
        create_playlist_request = self.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": playlist_name,
                    "description": "Created by SpotyTube."},
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = create_playlist_request.execute()
        playlist_id = response['id']
        return playlist_id

    def add_track_to_playlist(self, playlist_id, video_id):
        insert_vid_request = self.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        insert_vid_request.execute()
