import pygame as pg
import game_math as gm
import globs
import colors
import fonts
import shapes
from random import uniform, randint, choice


class Renderer:
    def __init__(self, screen_size):
        self.scaling = 2
        self.screen_size = screen_size
        self.display = pg.display.set_mode((1920, 1080), pg.RESIZABLE)
        self.lower_res = (
            self.screen_size[0] / self.scaling,
            self.screen_size[1] / self.scaling,
        )
        self.screen = pg.Surface(screen_size)
        self.trail_layer = pg.Surface(self.lower_res, pg.SRCALPHA)
        self.obstacle_layer = pg.Surface(screen_size, pg.SRCALPHA)
        self.text_layer = pg.Surface(screen_size, pg.SRCALPHA)
        self.display_fps_bool = True
        self.darken_trails_bool = True
        self.display_deaths_bool = True
        self.display_curve_bool = True

        # A layer used to darken trails
        self.darkener = pg.Surface(self.lower_res, flags=pg.SRCALPHA)
        self.darkener.fill((0, 0, 0, 30))
        self.light_darkener = pg.Surface(self.screen_size, flags=pg.SRCALPHA)
        self.light_darkener.fill((0, 0, 0, 2))

        self.trail_particles = list()  # [loc, vel(x,y), time]
        self.explosion_particles = list()  # loc, vel, time, size, color

    def update(self, dt, gameplay=True):
        self.screen.fill(colors.BLACK)
        self.screen.blit(self.obstacle_layer, (0, 0))
        new = pg.transform.scale(self.trail_layer, self.screen_size)
        self.screen.blit(new, (0, 0))
        if not globs.player.is_paused:
            globs.player.render()

        if gameplay:
            self.trail_particles_tick(dt)
            self.explosion_particles_tick(dt)

            if self.darken_trails_bool:
                self.darken_trails()
            if self.display_fps_bool:
                self.display_fps()
            if self.display_deaths_bool:
                self.display_deaths()
        elif not gameplay:
            self.screen.blit(self.text_layer, (0, 0))
            self.darken_layer(self.text_layer, light=True)

        self.display.blit(self.screen, (0, 0))
        # if self.display_curve_bool and gameplay:
        self.draw_curve(globs.player.get_curve(pg.mouse.get_pos()))
        # flip() updates the screen to make our changes visible
        pg.display.flip()

    def draw_line(self, start: pg.Vector2, end: pg.Vector2, color=colors.WHITE):
        pg.draw.line(self.trail_layer, color, start/self.scaling, end/self.scaling, width=10)

    def darken_trails(self):
        self.darken_layer(self.trail_layer)

    def darken_layer(self, layer, light=False):
        darkener = self.darkener if not light else self.light_darkener
        layer.blit(darkener, (0, 0), special_flags=pg.BLEND_RGBA_SUB)

    def clear_trails(self):
        self.trail_layer.fill((0, 0, 0, 255))

    def display_fps(self):
        fps = globs.clock.get_fps()
        fps = bytes(f"FPS:{fps:.3}", encoding="utf-8")
        font_text = fonts.FPS_FONT.render(fps, True, colors.WHITE)
        font_rect = font_text.get_rect(top=0, left=0)
        self.screen.blit(font_text, font_rect)
    
    def display_deaths(self):
        deaths = globs.player.deaths
        fps = bytes(f"Deaths:{deaths}", encoding="utf-8")
        font_text = fonts.FPS_FONT.render(fps, True, colors.WHITE)
        font_rect = font_text.get_rect(top=50, left=0)
        self.screen.blit(font_text,font_rect)

    def render_level(self, level: dict):
        self.obstacle_layer.fill(colors.BLACK)
        killers = level["killers"]
        finish = level["finish"]
        self.render_killers(killers, colors.RED)
        self.render_finish(finish, colors.GREEN)

    def render_killers(self, killers: dict, color):
        circle_killers = killers["circles"]
        rect_killers = killers["rects"]

        for circle in circle_killers:
            circle = shapes.Circle(*circle)
            self.render_circle(circle, color)

        for rect in rect_killers:
            rect = shapes.Rect(*rect)
            self.render_rect(rect, color)

    def render_finish(self, rect, color):
        finish_rect = shapes.Rect(*rect)
        self.render_rect(finish_rect, color)

    def render_circle(self, circle: shapes.Circle, color):
        if type(circle) == tuple:
            circle = shapes.Circle(*circle)
        pg.draw.circle(
            self.obstacle_layer,
            color,
            center=(circle.x, circle.y),
            radius=circle.radius,
        )

    def render_rect(self, rect: shapes.Rect, color):
        if type(rect) == tuple:
            rect = shapes.Rect(*rect)
        pg.draw.rect(
            self.obstacle_layer,
            color,
            rect=(rect.x, rect.y, rect.width, rect.height),
        )

    def draw_particle(self, center: pg.Vector2, color=colors.RED, size=5):
        pg.draw.circle(self.trail_layer, color, center=center, radius=size)

    def add_trail_particle(self, origin: pg.Vector2, direction: float, num=1):
        particle = [origin, direction, uniform(0.8, 1.3)]
        self.trail_particles.append(particle)

    def trail_particles_tick(self, dt):
        for particle in self.trail_particles:
            ps = globs.player.curve_speed * globs.player.curve_length / 600
            particle[0] = (particle[0][0] - particle[2] * (ps * 5 * particle[1][0])), (
                particle[0][1] - particle[2] * (ps * 5 * particle[1][1])
            )
            particle[1] = (particle[1][0] / 1.1, particle[1][1] / 1.1)
            particle[2] -= dt / 500
            if particle[2] <= 0:
                self.trail_particles.remove(particle)
                continue
            self.render_trail_particle(particle[0], particle[2])

    def render_trail_particle(self, particle_pos, time):
        color = time * 200
        size = 7 * time
        self.draw_particle(
            pg.Vector2(particle_pos[0] / self.scaling, particle_pos[1] / self.scaling),
            (color, 50, 50),
            (size + 5) / self.scaling,
        )

    def add_explosion_particles(self, origin: pg.Vector2, num=1):
        for _ in range(num):
            direction = pg.Vector2(randint(0, 20) / 10 - 1, randint(0, 20) / 10 - 1)
            particle = [
                origin,
                direction,
                uniform(0.8, 1.3),
                randint(5, 15),
                choice(colors.EXPLOSION_COLORS),
            ]
            self.explosion_particles.append(particle)

    def explosion_particles_tick(self, dt):
        for particle in self.explosion_particles:
            particle[0] = (particle[0][0] - particle[2] * (10 * particle[1][0])), (
                particle[0][1] - particle[2] * (10 * particle[1][1])
            )
            particle[2] -= dt / 1000
            if particle[2] <= 0:
                self.explosion_particles.remove(particle)
                continue
            self.render_explosion_particle(particle)

    def render_explosion_particle(self, particle):
        size = particle[2] * particle[3]
        self.draw_particle(
            pg.Vector2(particle[0][0] / self.scaling, particle[0][1] / self.scaling),
            particle[4],
            (size + 5) / self.scaling,
        )

    def explosion(self, origin: pg.Vector2):
        self.add_explosion_particles(origin, num=35)

    def draw_curve(self, curve):
        t = 0
        pos_1 = gm.bezier_calc_2d(curve, 0)
        while t < 1:
            pos_2 = gm.bezier_calc_2d(curve,t)
            pg.draw.line(self.display,colors.RED,pos_1, pos_2, width=5)
            pos_1 = pos_2
            t+=.1
            