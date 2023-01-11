import pygame as pg


def init(screen):
    global ASSET_PATH
    ASSET_PATH = "assets/"

    global SCREEN_SIZE
    SCREEN_SIZE = screen

    from rendering import Renderer
    from player import Player
    from level_handler import LevelHandler
    from collisions import Collider

    global player, renderer, clock, level_handler, collider
    renderer = Renderer(screen)
    clock = pg.time.Clock()
    player = Player()
    level_handler = LevelHandler()
    collider = Collider()

    from sounds import SoundHandler

    global sound
    sound = SoundHandler()

    global MAX_FPS
    MAX_FPS = 300
