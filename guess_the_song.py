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

def play_audio_from_youtube(song_url, play_time=24):
    mp3_file = download_and_convert_audio(song_url)
    
    if mp3_file:
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()
            print(f"Now playing... You have 20 seconds to guess!")

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

def add_more_songs(songs):
    while True:
        song_name = input("🎶 Enter song title (or type 'done' to stop): ")
        if song_name.lower() == 'done':
            break
        song_url = input("🔗 Enter the YouTube URL: ")
        songs[song_name] = song_url
        print(f"✅ '{song_name}' added successfully!")
        save_songs(songs)

def guess_the_song(songs):
    score = 0
    fastest_time = float('inf')
    fastest_player = "None"

    song_list = list(songs.items())  
    random.shuffle(song_list)  

    for song_title, song_url in song_list:
        print("Listen carefully! You have 20 seconds to recognize the song!")
        play_audio_from_youtube(song_url, play_time=24)  

        guess_start_time = time.time()
        guess_made = False

        while time.time() - guess_start_time < 30:
            guess = input(f"Your guess ({round(30 - (time.time() - guess_start_time))} seconds left): ")
            if guess.lower() == song_title.lower():
                guess_made = True
                elapsed_time = time.time() - guess_start_time
                print(f"Correct! You guessed it in {round(elapsed_time, 2)} seconds!")
                score += 1

                if elapsed_time < fastest_time:
                    fastest_time = elapsed_time
                    fastest_player = song_title
                break

        if not guess_made:
            print(f"Time's up! The correct answer was: {song_title}")

        if input("🎮 Continue playing? (y/n): ").lower() != 'y':
            break

    return score, fastest_time, fastest_player

def main_menu():
    songs = load_songs()

    score = 0
    fastest_time = float('inf')
    fastest_player = "None"

    while True:
        print("\n" + "-" * 50)
        print(" MAIN MENU ")
        print("1️ Play the game")
        print("2️ Add Songs")
        print("3 Check Score")
        print("4 Quit")
        print("-" * 50)
        
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            score, fastest_time, fastest_player = guess_the_song(songs)  
        elif choice == '2':
            add_more_songs(songs)  
        elif choice == '3':
            print(f"Your score: {score}")
            if fastest_time != float('inf'):
                print(f"Fastest guess: {fastest_player} in {round(fastest_time, 2)} seconds")
            else:
                print("No correct guesses yet! Let's get started!")
        elif choice == '4':
            print("Thanks for playing! See you next time!")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()