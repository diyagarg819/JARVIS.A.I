import os
from http.client import responses
from time import strftime
import speech_recognition as sr
import win32com.client
import webbrowser
import datetime
import random
import cohere

def ai(prompt):
    co = cohere.Client("hd6zS6rwQ73v2x4QQ1I5Z1KRywMhIkCP9VAs6k2D")
    text = f"Cohere response for prompt: {prompt} \n ********************************\n\n "

    response = co.chat(
        message=prompt,
        model='command-nightly',
        temperature=0.7
    )

    reply = response.text.strip()
    text += reply
    print(reply)

    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    return reply

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1.2
        audio = r.listen(source)
    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said : {query}")
        return query
    except Exception as e:
        return "Some Error Occured.Sorry from Jarvis"


time_spoken_count = 0

if __name__ == '__main__':
    print('Welcome')
    speaker.Speak("Hello I am Jarvis A.I. and how can I assist you")
    while True:
        print("Listening.....")
        query = takeCommand()
        query = query.lower().replace("chat gpt", "chatgpt").replace("jarvis", "").strip()

        # Define sites
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["instagram", "https://www.instagram.com/?hl=en"],
                 ["chatgpt", "https://chat.openai.com"]]

        # Open sites
        for site in sites:
            if any(word in query for word in [f"open {site[0]}", f"launch {site[0]}", site[0]]):
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break

        # Tell time only 2 times
        if "the time" in query.lower() and time_spoken_count < 2:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"Sir, the time is {strfTime}")
            time_spoken_count += 1

        # List of apps: [name_in_command, full_system_path]
        apps = [
            ["ms paint", "C:\\Windows\\System32\\mspaint.exe"],
            ["notepad", "C:\\Windows\\System32\\notepad.exe"],
            ["calculator", "C:\\Windows\\System32\\calc.exe"],
            ["chrome", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"],
            ["vs code", os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")]
        ]

        # Open apps
        for app in apps:
            if f"open {app[0]}" in query.lower():
                speaker.Speak(f"Opening {app[0]} sir...")
                os.startfile(app[1])
                break

        # AI response
        if "using artificial intelligence" in query.lower():
            ai(query)
            continue







