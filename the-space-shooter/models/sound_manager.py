import pygame as pg
from constants import (
    FIRE_SOUND,
    BGM_SOUND
)

class SoundManager:
    def __init__(self):
        """
        Initialize the Pygame mixer and load all sounds.
        """
        try:
            pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pg.error as e:
            print(f"Cannot initialize sound mixer: {e}")
            return
            
        # This dictionary will hold all our sound effects
        self.sounds = {}

        # --- Load Sound Effects (SFX) ---
        self.load_sfx("fire", FIRE_SOUND)
        
        self.load_sfx("explosion", FIRE_SOUND) 
        self.load_sfx("player_hit", FIRE_SOUND)

        # --- Load Background Music (BGM) ---
        self.bgm_path = BGM_SOUND

    def load_sfx(self, name, file_path):
        """
        Internal method to load a sound effect and store it.
        :param name: The key we'll use to play the sound (e.g., "fire")
        :param file_path: The path to the .ogg or .wav file
        """
        try:
            sound = pg.mixer.Sound(file_path)
            self.sounds[name] = sound
        except pg.error as e:
            print(f"Cannot load sound effect '{name}' from {file_path}: {e}")

    def play_music(self, loop=-1, volume=0.4):
        """
        Load and play background music.
        :param loop: -1 to loop forever
        :param volume: 0.0 to 1.0
        """
        try:
            pg.mixer.music.load(self.bgm_path)
            pg.mixer.music.set_volume(volume)
            pg.mixer.music.play(loop)
        except pg.error as e:
            print(f"Cannot play background music from {self.bgm_path}: {e}")

    def play_sfx(self, name, volume=0.5):
        """
        Play a sound effect from our dictionary.
        :param name: The key of the sound to play (e.g., "fire")
        :param volume: 0.0 to 1.0
        """
        if name in self.sounds:
            try:
                self.sounds[name].set_volume(volume)
                self.sounds[name].play()
            except pg.error as e:
                print(f"Cannot play sound effect '{name}': {e}")
        else:
            print(f"Sound effect '{name}' not found in SoundManager.")