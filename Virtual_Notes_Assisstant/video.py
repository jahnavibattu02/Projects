import os
import ffmpeg
import youtube_dl

def download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './audio.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def video(url):
    download(url)
    command = 'ffmpeg -i ./audio.mp3 -ab 160k -ar 44100 -vn ./audio.wav'
    os.system(command)
    os.remove('./audio.mp3')