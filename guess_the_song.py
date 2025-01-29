import random
import os
import yt_dlp
import pygame
import threading
import time 
import json

def load_songs(filename='songs.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return{}
    
def save_songs(songs, filename ='songs.json'):
    with open(filename, 'w') as file:
        json.dump(songs, file, indent=4)

songs = load_songs()

score = 0
played_songs = set()  # Tracks played songs

def play_song(song_path):
    playsound(song_path)

def ask_guess(correct_song_name):
    global score
    guess = input("Guess the song?: ")
    if guess.lower() == correct_song_name.lower():
        print("Correct!🎉")
        score += 1
    else:
        print(f"Wrong! The correct answer was: {correct_song_name}")

# Main game loop
if __name__ == "__main__":
    print("Welcome to the 'Guess the Song' Game!")
    print("It's 15s per song so try to guess what song is playing. Type your answer and hit Enter.")
    
    while True:
        # If all songs have been played, resets the played list and score
        if len(played_songs) == len(songs):
            print("Congratulations! All songs have been played! Resetting the list and your score.")
            played_songs.clear()
            score = 0  # Resets the score

        # Randomly selects a song that hasn't been played yet
        correct_song_name, song_path = random.choice(list(songs.items()))
        while correct_song_name in played_songs:
            correct_song_name, song_path = random.choice(list(songs.items()))

        # Plays the song
        play_song(song_path)
        played_songs.add(correct_song_name)  # Marks the song as played

        # Asks for a guess after the song ends
        ask_guess(correct_song_name)

        # Shows the current score
        print(f"Your current score is: {score}")

        # Asks if the player wants to play again
        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != "yes":
            break

    print("Thanks for playing! Your final score is:", score)
