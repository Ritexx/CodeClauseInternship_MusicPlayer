import os
import pygame
from tkinter import Tk, filedialog, Button, Label, Scale, Canvas

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
    
        self.root.geometry("400x400")  # Set the initial window size

        self.playlist = []
        self.current_track = 0

        self.canvas = Canvas(root, width=200, height=200)  # Create a canvas with size 200x200
        self.canvas.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights to center widgets
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

        self.load_button = Button(root, text="Load", command=self.load_music)
        self.load_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.play_button = Button(root, text="Play", command=self.play_music)
        self.play_button.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.pause_button = Button(root, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        self.stop_button = Button(root, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")

        self.volume_label = Label(root, text="Volume")
        self.volume_label.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="nsew")

        self.volume_slider = Scale(root, from_=0, to=1, resolution=0.1, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(0.5)  # Default volume set to 50%
        self.volume_slider.grid(row=2, column=3, padx=10, pady=10, columnspan=2, sticky="nsew")

        self.label = Label(root, text="")
        self.label.grid(row=3, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

    def load_music(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            self.playlist.append(file_path)
            self.label.config(text=f"Loaded: {os.path.basename(file_path)}")

    def play_music(self):
        if self.playlist:
            pygame.mixer.music.play()

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

root = Tk()
music_player = MusicPlayer(root)
root.mainloop()
