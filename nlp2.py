import google.generativeai as genai
import speech_recognition as sr
import win32com.client

API_KEY = 'AIzaSyCvCnR2aMcaZdaif1zVKBnZZborsbGYjOk'
genai.configure(api_key=API_KEY)
speaker = win32com.client.Dispatch("SAPI.SpVoice")
recognizer = sr.Recognizer()

def chat_with_gemini(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    print(response.text)
    speaker.Speak(response.text)

def listen_for_voice():
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        speaker.Speak(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speaker.Speak("Sorry, I did not understand that.")
    except sr.RequestError as e:
        speaker.Speak(f"Could not request results from Google Speech Recognition service; {e}")
    return None

if __name__ == "__main__":
    while True:
        user_input = listen_for_voice()
        if user_input:
            if user_input.lower() == "exit":
                speaker.Speak("Exiting...")
                break
            chat_with_gemini(user_input)
