import speech_recognition as sr
import webbrowser
import pyttsx3
import openai
import requests
from gtts import gTTS
import pygame
import os

# Install missing libraries: pip install requests openai gtts pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your Key Here>"

# Define musicLibrary manually or import from an external file
musicLibrary = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc"
}

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("temp.mp3")

def aiProcess(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant. Give short responses, please."},
            {"role": "user", "content": command}
        ]
    )
    return response["choices"][0]["message"]["content"]

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        link = musicLibrary.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find the song.")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Limit to top 5 headlines
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        recognizer = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Ya")
                
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")
