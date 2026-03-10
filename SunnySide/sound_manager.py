import pygame as pg
from constants import SOUND_PATH
import os

class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
            
        # Initialize mixer if not already done
        if not pg.mixer.get_init():
            pg.mixer.init()
            
        self.sounds = {}
        self.load_sounds()
        self.initialized = True

    def load_sounds(self):
        # We pre-load sounds into memory
        try:
            self.sounds['coin'] = pg.mixer.Sound(os.path.join(SOUND_PATH, "coin.wav"))
            self.sounds['attack'] = pg.mixer.Sound(os.path.join(SOUND_PATH, "attack.wav"))
            # Set volume optionally, 0.0 to 1.0
            self.sounds['coin'].set_volume(0.5)
            self.sounds['attack'].set_volume(1)
        except FileNotFoundError:
            print("Warning: coin.wav not found. Check the path.")

    def play(self, sound_name):
        """Play a loaded sound effect by name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Warning: Sound '{sound_name}' not loaded.")

# Global instance
sound_manager = SoundManager()
