import random
import os
import yt_dlp
import pygame
import time 
import json
import subprocess
import tempfile

def load_songs(filename='songs.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return{}
    
def save_songs(songs, filename ='songs.json'):
    with open(filename, 'w') as file:
        json.dump(songs, file, indent=4)

def download_and_convert_audio(song_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tempfile.mktemp(suffix='.webm'),
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(song_url, download=True)
            temp_file_path = ydl.prepare_filename(info_dict)
            mp3_file_path = temp_file_path.replace(".webm", ".mp3")

            with open(os.devnull, 'w') as devnull:
                subprocess.run(['ffmpeg', '-i', temp_file_path, '-vn', '-acodec', 'libmp3lame', mp3_file_path], check=True, stdout=devnull, stderr=devnull)

            os.remove(temp_file_path)
            return mp3_file_path

    except Exception as e:
        print(f"⚠️ Error downloading audio: {e}")
        return None
