import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary   # make sure in same folder you should created a file for music with (musicLibrary)
import requests
import os
import subprocess
import platform
import ctypes
from difflib import get_close_matches

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "your_newsapi_key_here"   # Replace with your own NewsAPI Key

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c=c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("chrome://newtab/")
        
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")

    elif "open linkedin" in c:
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com/feed/")

    elif "open leetcode" in c:
        speak("Opening Leetcode")
        webbrowser.open("https://leetcode.com/problemset/")

    elif "open chatgpt" in c:
        speak("Opening Chatgpt")
        webbrowser.open("https://chatgpt.com/")

    elif "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("https://github.com/dashboard")

    elif "open instagram" in c:
        speak("Opening Instagram")
        os.startfile(r"C:\Path\To\Instagram.link")  # Update the path to where Instagram shortcut is saved on your PC

    elif "open vs code" in c:
        speak("Opening VS Code")
        os.startfile(r"C:\Path\To\Visual Studio Code.lnk")  # Update the path to where Vs Code is saved on your PC

    elif "open spotify" in c:
        speak("Opening Spotify")
        os.startfile(r"C:\Path\To\Spotify.lnk")  # Update the path to where Spotify shortcut is saved on your PC

    elif "shutdown" in c.lower():
        speak("Shutting down the system.")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Linux":
            os.system("shutdown now")

    elif c.startswith("play"):
        try:
            song = c.replace("play", "").strip()
            match = get_close_matches(song, musicLibrary.music.keys(), n=1, cutoff=0.5)
            if match:
                link = musicLibrary.music[match[0]]
                speak(f"Playing {match[0]}")
                webbrowser.open(link)
            else:
                speak("Sorry, I couldn't find that song.")
        except Exception as e:
            speak("Couldn't play the song.")
            print("Error:", e)

    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data["articles"]
            print("Top Headlines:\n")
        for i, article in enumerate(articles[:5], start=1):  # First 5 headlines
            speak(f"{i}. {article['title']}")
        else:
            print("Error:", r.status_code, r.text)

    elif "close browser" in c.lower() or "all types" in c.lower() or "close all tab" in c.lower():
        speak("Closing all browser tabs.")
        browsers = ["chrome.exe", "msedge.exe", "firefox.exe"]
        for b in browsers:
            os.system(f"taskkill /f /im {b}")


# Fuzzy match for commands like "open insta", "launch code"....
    else:
        command_keywords = {
            "google": "https://www.google.com/",
            "youtube": "https://www.youtube.com/",
            "linkedin": "https://www.linkedin.com/feed/",
            "leetcode": "https://leetcode.com/problemset/",
            "chatgpt": "https://chatgpt.com/",
            "github": "https://github.com/dashboard",
            "instagram": "https://www.instagram.com/",
            "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
        }

    match = get_close_matches(c, command_keywords.keys(), n=1, cutoff=0.5)
    if match:
        link = command_keywords[match[0]]
        speak(f"Opening {match[0]}")
        webbrowser.open(link)
    else:
        print(c)

if __name__ == "__main__" :
    speak("Initializing Jarvis...")
    while True:
    # Listen for the wake word "Jarvis"
    #obtain audio from the microphone
        r=sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio= r.listen(source, timeout=3, phrase_time_limit=5)
            word= r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
