from ast import excepthandler
from cgitb import text
import pygame as pg
import le_text_displayer
import globs
import colors

pg.init()
pg.mixer.init()
screen_size = (1920, 1080)
pg.display.set_caption("Bezi")

globs.init(screen_size)
player = globs.player
renderer = globs.renderer
clock = globs.clock
level_handler = globs.level_handler

level_handler.load_level(0)

texter = le_text_displayer.LETexter()

location1 = None
location2 = None

selected = None
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_t:
                texter.notify("Test")
            elif event.key == pg.K_1:
                texter.notify("Deathrect Selected")
                selected = "deathrect"
            elif event.key == pg.K_2:
                texter.notify("Deathcircle Selected")
                selected = "deathcircle"
            elif event.key == pg.K_3:
                texter.notify("Finish Selected")
                selected = "finish"
            elif event.key == pg.K_f:
                texter.notify("Demolish Selected")
                selected = "demolish"
            elif event.key == pg.K_s:
                texter.notify("Starting position Selected")
                selecting = "staring_position"
            elif event.key == pg.K_x:
                level_handler.write_level()
                texter.notify("LEVEL WRITTEN")
            elif event.key == pg.K_RIGHT:
                texter.notify("incrementing level")
                level_handler.current_level += 1
                try:
                    level_handler.load_level()
                except:
                    level_handler.make_file(level_handler.current_level)
            elif event.key == pg.K_LEFT:
                texter.notify("decrementing level")
                if level_handler.current_level > 0:
                    level_handler.current_level -= 1
                level_handler.load_level()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                location1, location2 = None, None
                continue
            if selected == "staring_position":
                level_handler.set_start(event.pos)
                player.set_defaults()
                continue
            if selected == "demolish":
                level_handler.demolish(event.pos)
                continue
            if selected == "finish":
                x, y = event.pos
                level_handler.level["finish"] = x, y, 50, 50
                continue
            if location1 == None:
                texter.notify("Position 1 Selected")
                location1 = event.pos
                continue
            else:
                texter.notify("Position 2 Selected")
                location2 = event.pos
            if selected == "deathrect":
                level_handler.add_rect_killer(location1, location2)
            elif selected == "deathcircle":
                level_handler.add_circle_killer(location1, location2)
            location1, location2 = None, None

    renderer.render_level(level_handler.level)

    if selected == "deathrect":
        if location1 != None and location2 == None:
            renderer.render_rect(
                level_handler.make_rect(location1, pg.mouse.get_pos()), colors.GRAY
            )
    elif selected == "deathcircle":
        if location1 != None and location2 == None:
            renderer.render_circle(
                level_handler.make_circle(location1, pg.mouse.get_pos()), colors.GRAY
            )

    renderer.update(0, gameplay=False)

pg.quit()
