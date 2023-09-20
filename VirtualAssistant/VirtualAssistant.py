import os
import subprocess
import speech_recognition
import requests
import pyttsx3
import json
import datetime


def print_speak(engine, text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def setup():
    global engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 270)

    print_speak(engine, ">Code Libraries loaded")

    print_speak(engine, ">Setting up environment")
    global priorinfo
    priorinfo = json.load(open('prior_info.json', "r"))

    global URL
    URL = "https://chatgpt-api8.p.rapidapi.com/"

    global headers
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.environ.get("APIKEY"),
        "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

    global term_size
    term_size = os.get_terminal_size()

    print_speak(engine, ">Awaiting commands")
    print("_" * term_size.columns)


def loop():
    kill_flag = False
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone(0) as source:
        while not kill_flag:
            r.pause_threshold = .7
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
                if "exit program" in query:
                    print_speak(engine, ">Exiting Program...")
                    kill_flag = True
                    break
                else:
                    payload = [
                        {
                            "content": f"{query}",
                            "role": "user"
                        }
                    ]
                    print_speak(engine, query)
                    print_speak(engine, ">Generating Response...")
                    response = requests.post(
                        URL, json=payload, headers=headers)
                    print_speak(engine, response.json()["text"])
                    print("_" * term_size.columns)
            except:
                print("_")


def wrap_up():

    saving_configs = {
        "PreviousTimeAtClose": str(datetime.datetime.now())
    }
    with open('prior_info.json', "w") as f:
        json.dump(saving_configs, f)


def main():
    setup()
    loop()
    wrap_up()


if __name__ == "__main__":
    main()
