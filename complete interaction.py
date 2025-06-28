import threading
import time
import cv2
import numpy as np
import yt_dlp
import vlc
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
import win32com.client
# Configure Google Generative AI
API_KEY = 'AIzaSyCvCnR2aMcaZdaif1zVKBnZZborsbGYjOk'  # Replace with your API key
genai.configure(api_key=API_KEY)
speaker = win32com.client.Dispatch("SAPI.SpVoice")
# Music Player Functionality
class MusicPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.playlist = []
        self.current_song = None

    def search_song(self, song_name):
        ydl_opts = {'format': 'bestaudio', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{song_name}", download=False)
            if not search_results['entries']:
                return None, None
            song_url = search_results['entries'][0]['url']
            song_title = search_results['entries'][0]['title']
            return song_url, song_title

    def play_song(self, song_url, song_title):
        self.current_song = song_title
        self.player.set_mrl(song_url)
        speaker.Speak(f"Playing '{song_title}'...")
        self.player.play()

    def pause(self):
        speaker.Speak("Pausing song.")
        self.player.pause()

    def resume(self):
        speaker.Speak("Resuming song.")
        self.player.play()

    def stop(self):
        speaker.Speak("Stopping song.")
        self.player.stop()

    def set_volume(self, volume_level):
        if 0 <= volume_level <= 100:
            self.player.audio_set_volume(volume_level)
            speaker.Speak(f"Volume set to {volume_level}.")
        else:
            speaker.Speak("Volume level must be between 0 and 100.")

    def main(self):
        speaker.Speak("Music Player Module")
        song_name = input("Enter the song name to play: ")
        song_url, song_title = self.search_song(song_name)
        if song_url:
            self.play_song(song_url, song_title)
        else:
            speaker.Speak("Song not found.")

# Robot Control Functions
def move_forward():
    speaker.Speak("Robot: Moving forward")

def turn_left():
    speaker.Speak("Robot: Turning left")

def turn_right():
    speaker.Speak("Robot: Turning right")

ACTION_FUNCTIONS = {
    "move_forward": move_forward,
    "turn_left": turn_left,
    "turn_right": turn_right,
}

def detect_obstacle(frame, back_sub, threshold=3000):
    fg_mask = back_sub.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > threshold:
            return "obstacle_in_front"
    return "clear_path"

def robot_main():
    speaker.Speak("Robot Cleaning Module")
    back_sub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
    cap = cv2.VideoCapture(0)
    speaker.Speak("Robot cleaning in progress...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        state = detect_obstacle(cv2.resize(frame, (320, 240)), back_sub)
        if state == "clear_path":
            move_forward()
        else:
            turn_left()
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()

# Chatbot Interaction
def chat_with_gemini(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text

def chatbot_main(command):
    speaker.Speak("Welcome to Chatbot! Type 'exit' to quit.")
    while True:

        if command.lower() in ["exit", "quit"]:
            speaker.Speak("Exiting Chatbot. Goodbye!")
            break
        response = chat_with_gemini(command)
        speaker.Speak(f"AI: {response}")

# Main Controller
class Controller:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.running = True
        self.music_player = MusicPlayer()
        self.back_sub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
        self.cap = cv2.VideoCapture(0)

    def voice_recognition_loop(self):
        while self.running:
            try:
                with sr.Microphone() as source:
                    speaker.Speak("Listening for commands...")
                    audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                print(command)
                speaker.Speak(command)
                self.handle_voice_command(command)
            except Exception as e:
                speaker.Speak(f"Voice recognition error: {e}")

    def handle_voice_command(self, command):
        if "play song" in command:
            song_name = command.replace("play song", "").strip()
            speaker.Speak(f"Voice Command: Play Song - {song_name}")
            song_url, song_title = self.music_player.search_song(song_name)
            if song_url:
                self.music_player.play_song(song_url, song_title)
            else:
                speaker.Speak("Song not found.")
        elif "pause song" in command:
            self.music_player.pause()
        elif "resume song" in command:
            self.music_player.resume()
        elif "stop song" in command:
            self.music_player.stop()
        elif "set volume" in command:
            try:
                volume = int(command.split("to")[-1].strip())
                self.music_player.set_volume(volume)
            except ValueError:
                speaker.Speak("Invalid volume command.")
        elif "clean floor" in command:
            speaker.Speak("Voice Command: Clean Floor")
            robot_main()
        elif "chat" in command:
            speaker.Speak("Voice Command: Chat")
            chatbot_main(command)
        else:
            speaker.Speak("Unknown command, please try again.")

    def run(self):
        threading.Thread(target=self.voice_recognition_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

# Main Execution
if __name__ == "__main__":
    controller = Controller()
    try:
        controller.run()
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        speaker.Speak("Exiting program...")
    finally:
        controller.stop()
