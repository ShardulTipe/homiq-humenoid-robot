import yt_dlp
import vlc
import time
import threading
import speech_recognition as sr
import sys

class MusicPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.playlist = []
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.playback_thread = None
        self.current_song = None

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Listening for your command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

    def search_song(self, song_name):
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if not search_results['entries']:
                print("Song not found.")
                return None, None

            song_url = search_results['entries'][0]['url']
            song_title = search_results['entries'][0]['title']
            return song_url, song_title

    def play_song(self, song_url, song_title):
        self.current_song = song_title
        self.player.set_mrl(song_url)
        print(f"Playing '{song_title}' from YouTube...")
        self.player.play()

    def pause_song(self):
        if self.player.is_playing():
            self.player.pause()
            print("Playback paused.")
        else:
            print("No song is currently playing.")

    def resume_song(self):
        if not self.player.is_playing() and self.player.get_state() == vlc.State.Paused:
            self.player.play()
            print("Playback resumed.")
        else:
            print("No song is paused.")

    def set_volume(self, level):
        if self.player:
            self.player.audio_set_volume(level)
            print(f"Volume set to {level}.")

    def add_song_to_playlist(self, song_name):
        song_url, song_title = self.search_song(song_name)
        if song_url:
            self.playlist.append((song_url, song_title))
            print(f"'{song_title}' added to playlist.")

    def play_playlist(self):
        for song_url, song_title in self.playlist:
            self.play_song(song_url, song_title)
            while self.player.is_playing():
                time.sleep(1)  # Wait until the song finishes
        print("Playlist finished.")

    def start_listening(self):
        self.is_listening = True
        threading.Thread(target=self.listen_for_commands, daemon=True).start()

    def stop_listening(self):
        self.is_listening = False
        print("Stopped listening.")
        sys.exit()


    def listen_for_commands(self):
        while self.is_listening:
            command = self.recognize_speech()
            if command:
                self.handle_command(command)

    def handle_command(self, command):
        if "add song to playlist" in command:
            print("Say the name of the song to add to the playlist...")
            song_name = self.recognize_speech()
            if song_name:
                self.add_song_to_playlist(song_name)
        elif command.startswith("play song"):
            song_name = command.replace("play song", "").strip()
            if song_name:
                print(f"Searching and playing the song '{song_name}'...")
                song_url, song_title = self.search_song(song_name)
                if song_url:
                    self.play_song(song_url, song_title)
                else:
                    print("Could not find the song.")
        elif "play playlist" in command:
            if self.playback_thread and self.playback_thread.is_alive():
                print("Playlist is already playing.")
            else:
                self.playback_thread = threading.Thread(target=self.play_playlist)
                self.playback_thread.start()
        elif "pause" in command:
            self.pause_song()
        elif "resume" in command:
            self.resume_song()
        elif "set volume to" in command:
            level_str = command.replace("set volume to", "").strip()
            volume_level = self.parse_volume(level_str)
            if volume_level is not None:
                self.set_volume(volume_level)
            else:
                print("Please specify a volume level of 0, 10, 20, ..., or 100.")
        elif "stop" in command:
            self.stop_listening()
            self.player.stop()
            if self.player:
                self.player.stop()
        else:
            print("Command not recognized. Please try again.")

    def parse_volume(self, level_str):
        volume_map = {
            "zero": 0, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40,
            "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100
        }

        if level_str in volume_map:
            return volume_map[level_str]

        if level_str.isdigit():
            level = int(level_str)
            if level in range(0, 101, 10):
                return level

        return None  # Invalid volume level


def main():
    player = MusicPlayer()

    try:
        player.start_listening()  # Start listening for voice commands
        while True:
            pass  # Keeps the main thread active while background threads handle music and commands
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
    finally:
        player.stop_listening()  # Ensure we stop listening when done
        if player.player:
            player.player.stop()  # Stop any song that's currently playing


if __name__ == "__main__":
    main()
