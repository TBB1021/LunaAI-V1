import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from LunaAI import LunaAi
#creates the spotify plugin
class Plugin():
    def __init__(self):
        self.commands = {"play song on Spotify": self.Play_Song,"pause music": self.Pause_music,"continue song": self.Resume_Song,"skip song": self.Next_Song,"Go back": self.Previous_Song}
        client_ID = os.getenv('SpotUser')
        client_secret = os.getenv('spotSecret')
        self.spot_connection = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_ID,client_secret=client_secret,redirect_uri="https://192.168.4.116:8000/callback",scope='user-read-playback-state user-modify-playback-state user-read-currently-playing'))
        devices = self.spot_connection.devices()["devices"]
        self.device_ID = devices[0]['id']
        self.luna=LunaAi()
        self.spot_connection.transfer_playback(self.device_ID, force_play=False)

    #checks to see if any commands are a match
    def Command_Words_Check(self, chosen_command):
        return chosen_command in self.commands

    #executes the given command
    def Execute(self, command, prompt=None):
        if command in self.commands:
            return self.commands[command](prompt)
    #grabs user's song and plays it on shuffle with other songs
    def Play_Song(self, prompt):
        prompt = prompt.lower()
        for text in ["play", "on spotify", "music", "song"]:
            prompt = prompt.replace(text, "")
        search = prompt.strip()
        if search:
            result = self.spot_connection.search(q=search, limit=1, type='track')
            if result["tracks"]["items"]:
                track = result["tracks"]["items"][0]
                track_uri = track["uri"]
                album_uri = track["album"]["uri"]

                self.spot_connection.shuffle(True, self.device_ID)
                self.spot_connection.start_playback(
                    device_id=self.device_ID,
                    context_uri=album_uri,
                    offset={"uri": track_uri}
                )
            else:
                self.luna.TextToSpeech("Sorry No Song Could be found")

    #continues the song
    def Resume_Song(self, prompt):
        self.spot_connection.start_playback(device_id=self.device_ID)
    #plays the next song
    def Next_Song(self, prompt):
        self.spot_connection.next_track()
    #plays the previous song
    def Previous_Song(self, prompt):
        try:
            self.spot_connection.previous_track()
        except spotipy.exceptions.SpotifyException as e:
            self.luna.TextToSpeech("failed")
    #pauses the song
    def Pause_music(self, prompt):
        self.spot_connection.pause_playback(device_id=self.device_ID)
