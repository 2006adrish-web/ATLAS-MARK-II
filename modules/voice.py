import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import edge_tts
from playsound import playsound
import asyncio
import time
import os

recognizer = sr.Recognizer()

VOICE = "en-GB-RyanNeural"


def listen():

    fs = 44100
    duration = 5

    print("\n🎤 Listening...\n")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write("voice.wav", fs, recording)

    with sr.AudioFile("voice.wav") as source:
        audio = recognizer.record(source)

    try:

        print("⚡ Recognizing...\n")

        command = recognizer.recognize_google(audio)

        print(f"YOU SAID: {command}")

        return command.lower()

    except sr.UnknownValueError:

        speak("I could not understand you.")

        return ""

    except sr.RequestError:

        speak("Speech recognition service failed.")

        return ""


def type_print(text):

    for char in text:

        print(char, end="", flush=True)

        time.sleep(0)

    print()


def speak(text):

    clean_text = text.replace("*", "")
    clean_text = clean_text.replace("#", "")
    clean_text = clean_text.replace("`", "")

    print("\nATLAS:\n")

    type_print(clean_text)

    async def edge_speak():

        filename = f"voice_{int(time.time())}.mp3"

        communicate = edge_tts.Communicate(
            clean_text,
            VOICE
        )

        await communicate.save(filename)

        return filename

    try:

        filename = asyncio.run(edge_speak())

        playsound(filename)

        os.remove(filename)

    except Exception as e:

        print("VOICE ERROR:", e)