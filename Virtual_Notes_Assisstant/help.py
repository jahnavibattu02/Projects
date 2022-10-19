import matplotlib.pyplot as plt
import librosa
from pathlib import Path
import sounddevice as sd
import wavio
import requests
import speech_recognition

def stt(filename):
    path = './'+filename
    r = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
        return text

def read_audio(file):
    with open(file, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return audio_bytes

def record(duration=15, fs=48000):
    sd.default.samplerate = fs
    sd.default.channels = 1
    myrecording = sd.rec(int(duration * fs))
    sd.wait(duration)
    return myrecording

def save_record(path_myrecording, myrecording, fs):
    wavio.write(path_myrecording, myrecording, fs, sampwidth=2)
    return None

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()