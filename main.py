from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse

# GPT key
openai.api_key = "your-api-key-here"

# TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return "Sorry, I didn't catch that."

def ask_gpt(prompt):
    try:
        messages = [{"role": "system", "content": "You are Jarvis, a helpful assistant."},
                    {"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Sorry, I couldn't reach GPT."

def detect_command(query):
    query = query.lower()
    if "play" in query:
        song = query.replace("play", "").strip()
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
        webbrowser.open(url)
        return f"Playing {song} on YouTube"

    elif "search" in query:
        topic = query.replace("search", "").strip()
        url = f"https://www.google.com/search?q={urllib.parse.quote(topic)}"
        webbrowser.open(url)
        return f"Searching for {topic}"

    else:
        return None

class JarvisApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("jarvis.kv")

    def run_jarvis(self):
        user_input = listen()
        self.root.ids.chat.text += f"\n\nYou: {user_input}"
        action_result = detect_command(user_input)
        if action_result:
            speak(action_result)
            self.root.ids.chat.text += f"\nJarvis: {action_result}"
        else:
            response = ask_gpt(user_input)
            speak(response)
            self.root.ids.chat.text += f"\nJarvis: {response}"

if __name__ == '__main__':
    JarvisApp().run()
