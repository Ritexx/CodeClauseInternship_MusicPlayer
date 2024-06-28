import os
import pygame
from tkinter import Tk, filedialog, Button, Label, Scale, Frame, Listbox, Scrollbar
from tkinter.ttk import Progressbar

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x400")  # Set the initial window size 
        
        self.playlist = []
        self.current_track = 0
        self.music_length = 0

        pygame.mixer.init()

        # Display Current Track Label
        self.status_label = Label(root, text="", wraplength=550)
        self.status_label.pack()

        # Setting top margin after packing
        self.status_label.pack_configure(pady=(20, 10))

        # Progress Name Label (to display current track name)
        self.progress_name = Label(root, text="", wraplength=550)
        self.progress_name.pack()

        # Progress Bar
        self.progress_bar = Progressbar(root, orient="horizontal", length=550, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Control Buttons
        self.control_frame = Frame(root)
        self.control_frame.pack(pady=10)

        self.previous_button = Button(self.control_frame, text="Previous", command=self.previous_track, width=10)
        self.previous_button.grid(row=0, column=0, padx=5)

        self.play_button = Button(self.control_frame, text="Play", command=self.play_music, width=10)
        self.play_button.grid(row=0, column=1, padx=5)

        self.pause_button = Button(self.control_frame, text="Pause", command=self.pause_music, width=10)
        self.pause_button.grid(row=0, column=2, padx=5)

        self.next_button = Button(self.control_frame, text="Next", command=self.next_track, width=10)
        self.next_button.grid(row=0, column=3, padx=5)

        self.stop_button = Button(self.control_frame, text="Stop", command=self.stop_music, width=10)
        self.stop_button.grid(row=0, column=4, padx=5)

        # Volume Slider and Load Button
        volume_frame = Frame(root)
        volume_frame.pack(pady=10)

        self.volume_label = Label(volume_frame, text="Volume:")
        self.volume_label.grid(row=0, column=0, padx=5)

        self.volume_slider = Scale(volume_frame, from_=0, to=1, resolution=0.05, orient="horizontal", command=self.set_volume, length=200)
        self.volume_slider.set(0.5)  # Default volume set to 50%
        self.volume_slider.grid(row=0, column=1, padx=5)

        self.load_button = Button(volume_frame, text="Load", command=self.load_music, width=10)
        self.load_button.grid(row=0, column=2, padx=5)

        # Playlist Frame
        playlist_frame = Frame(root)
        playlist_frame.pack(pady=10, padx=10, fill="x", expand=True)

        self.playlist_label = Label(playlist_frame, text="Playlist")
        self.playlist_label.pack()

        self.playlist_listbox = Listbox(playlist_frame, selectmode="single", width=70, height=20)
        self.playlist_listbox.pack(side="left", fill="both", expand=True)
        self.playlist_listbox.bind("<Double-1>", self.play_selected_track)

        self.scrollbar = Scrollbar(playlist_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.playlist_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.playlist_listbox.yview)

        self.update_progress()

    def load_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for file_path in file_paths:
            if file_path:
                self.playlist.append(file_path)
                self.update_playlist()
                self.music_length = pygame.mixer.Sound(file_path).get_length()
                self.update_progress()

    def play_music(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            current_track_name = os.path.basename(self.playlist[self.current_track])
            self.progress_name.config(text=f"Now Playing: {current_track_name}")

    def play_selected_track(self, event):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            self.current_track = selected_index[0]
            self.play_music()

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_progress(self):
        current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
        if current_time >= 0 and self.music_length > 0:
            progress_percentage = (current_time / self.music_length) * 100
            self.progress_bar["value"] = progress_percentage
        else:
            self.progress_bar["value"] = 0
        self.root.after(100, self.update_progress)  # Update every 100 milliseconds

    def update_playlist(self):
        self.playlist_listbox.delete(0, "end")
        for song in self.playlist:
            self.playlist_listbox.insert("end", os.path.basename(song))

    def previous_track(self):
        if len(self.playlist) > 1:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.play_music()

    def next_track(self):
        if len(self.playlist) > 1:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.play_music()

if __name__ == "__main__":
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
