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

def play_audio_from_youtube(song_url, play_time=15):
    mp3_file = download_and_convert_audio(song_url)
    
    if mp3_file:
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            print(f"Now playing... You have {play_time} seconds to guess!")

            start_time = time.time()
            while time.time() - start_time < play_time:
                if not pygame.mixer.music.get_busy():
                    break
                time.sleep(0.1)

            pygame.mixer.music.stop()
            print("Song ended! Time to guess!")

        except Exception as e:
            print(f"Error during audio playback: {e}")
        
        pygame.mixer.quit()
        time.sleep(1)

        try:
            os.remove(mp3_file)
        except PermissionError:
            time.sleep(2)
            try:
                os.remove(mp3_file)
            except Exception as e:
                print(f"Error deleting file: {e}")
    else:
        print("Oops! Couldn't load the song.")