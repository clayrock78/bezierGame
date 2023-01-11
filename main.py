import pygame as pg
import globs
from time import perf_counter

pg.init()
pg.mixer.init()
screen_size = (1920, 1080)
pg.display.set_caption("Bezi")

globs.init(screen_size)
player = globs.player
renderer = globs.renderer
clock = globs.clock
level_handler = globs.level_handler


level = level_handler.load_level(0)
renderer.render_level(level)
player.set_defaults()

dt = 0
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            player.update_curve(event.pos)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_s:
                level_handler.advance_level()
                player.set_defaults()

    globs.renderer.update(dt)

    dt = clock.tick(globs.MAX_FPS)
    player.tick(dt / 1000)


pg.quit()
