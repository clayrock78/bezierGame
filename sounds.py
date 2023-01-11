import pygame as pg
import globs
from random import choice


class SoundHandler:
    def __init__(self):
        pg.mixer.init()
        self.character_death_sounds = [
            pg.mixer.Sound(f"{globs.ASSET_PATH}death_sound.wav"),
            pg.mixer.Sound(f"{globs.ASSET_PATH}death_sound1.wav"),
            pg.mixer.Sound(f"{globs.ASSET_PATH}death_sound2.wav"),
        ]
        for sound in self.character_death_sounds:
            sound.set_volume(0.125)

    def play_death_sound(self):
        sound = choice(self.character_death_sounds)
        sound.play()
