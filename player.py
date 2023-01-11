import pygame as pg
import sprite
import game_math as gm
from math import atan2, sin, cos, pi
from random import uniform
import globs


class Player:
    prev_x: float = 0
    prev_y: float = 0
    x: float = 0
    y: float = 0
    heading: float = 0
    # three points in 2d space, p0, p1, p2
    curve = [(0, 0), (0, 0), (0, 0)]
    curve_length = 1
    curve_speed = 1
    is_moving = False
    is_paused = False
    t: float = 0
    speed: float = 15
    sprite: sprite.Sprite
    bezier_extension: float = 350
    draw_trail: bool = False
    original_collision_points = [(-25, 0), (25, -25), (25, 25)]
    pause_time = 0
    tick_state = 0
    deaths = 0

    def __init__(
        self,
    ) -> None:
        self.sprite = sprite.Sprite()
        # self.update_curve()
        self.is_moving = False

    def set_defaults(self) -> None:
        self.x, self.y, self.heading = globs.level_handler.get_starting_pos()
        self.pause_time = 0
        self.is_moving = False
        self.curve = [(0, 0), (0, 0), (0, 0)]
        self.t = 0
        self.curve_length = 0
        self.is_paused = False
        self.sprite.rotate_image(self.heading)
        self.render()

    def tick(self, dt: float) -> None:
        # self.speed = gm.len_linear_2d((self.prev_x, self.prev_y), (self.x, self.y))
        self.tick_state = (self.tick_state + 1) % 3

        if self.is_paused:
            self.pause_time -= dt
            if self.pause_time < 0:
                self.set_defaults()
            return

        if self.is_moving == False:
            return

        self.t += dt * self.curve_speed
        if self.t > 1:
            self.prev_x, self.prev_y = self.x, self.y
            self.move_forward(dt)
        else:
            self.prev_x, self.prev_y = self.x, self.y
            self.x, self.y = gm.bezier_calc_2d(self.curve, self.t)
            self.heading = atan2(self.y - self.prev_y, self.x - self.prev_x)
            self.sprite.rotate_image(self.heading)

            if self.t + dt > 1:
                self.speed = gm.len_linear_2d(
                    pg.Vector2(self.prev_x, self.prev_y), pg.Vector2(self.x, self.y)
                )

        collision_points = self.get_collision_points()
        collision = globs.collider.do_player_collisions(collision_points)

        if collision["death"] or self.world_bound_collision_bool():
            self.death()

        if collision["winning"]:
            globs.level_handler.advance_level()
            self.set_defaults()

        if self.draw_trail:
            globs.renderer.draw_line(pg.Vector2(self.prev_x, self.prev_y), pg.Vector2(self.x, self.y))
        if self.tick_state == 0:
            self.particle_trail()

    def get_curve(self, click_pos):
        curve = [(0, 0), (0, 0), (0, 0)]
        curve[0] = pg.Vector2(self.get_loc())
        curve[1] = pg.Vector2(
            self.x + self.bezier_extension * cos(self.heading),
            self.y + self.bezier_extension * sin(self.heading),
        )
        curve[2] = pg.Vector2(click_pos)
        return curve

    def update_curve(self, click_pos: pg.Vector2 = (0, 0)) -> None:
        "Updates all information relevant to the curve of the player"
        if self.is_paused:
            return

        self.is_moving = True
        self.t = 0
        click_distance = gm.len_linear_2d(pg.Vector2(self.get_loc()), pg.Vector2(click_pos))
        # Update the handles of the bezier curve
        self.curve = self.get_curve(click_pos)
        self.curve_length = gm.approximate_bez_curve_len(self.curve)

        # self.curve_length = gm.len_linear_2d(self.curve[0], self.curve[2])

    def get_loc(self) -> pg.Vector2:
        "Returns the x and y coordinates of the player"
        return (self.x, self.y)

    def render(self) -> None:
        "Renders the character to the screen"
        globs.renderer.screen.blit(
            self.sprite.image, self.sprite.image.get_rect(center=self.get_loc())
        )
        # globs.renderer.trail_layer.blit(self.sprite.image, , self.sprite.image.get_rect(center=self.get_loc()))

    def move_forward(self, dt) -> None:
        "Moves the player in the direction they are facing"
        self.x += self.speed * cos(self.heading) * dt * 50
        self.y += self.speed * sin(self.heading) * dt * 50

    def world_bound_collision_dict(self, world_size: tuple[int, int]) -> dict:
        "Return a dictionary of collisions with the world boundaries"
        collisions = {"up": False, "down": False, "left": False, "right": False}
        if self.x < 0:
            collisions["left"] = True
        if self.y < 0:
            collisions["up"] = True
        if self.x > world_size[0]:
            collisions["right"] = True
        if self.y > world_size[1]:
            collisions["down"] = True
        return collisions

    def world_bound_collision_bool(self) -> bool:
        "Returns a boolean indicating collision with any world boundary"
        world_size = globs.SCREEN_SIZE
        if self.x < 0:
            return True
        if self.y < 0:
            return True
        if self.x > world_size[0]:
            return True
        if self.y > world_size[1]:
            return True
        return False

    def get_collision_points(self):
        pos = (self.x, self.y)
        collision_points = [
            gm.rotate_point(gm.tuplesub(pos, cp), pg.Vector2(pos), self.heading)
            for cp in self.original_collision_points
        ]
        return collision_points

    def death(self):
        self.deaths += 1 
        self.is_moving = False
        self.is_paused = True
        self.pause_time = 0.5
        globs.sound.play_death_sound()
        globs.renderer.explosion((self.x, self.y))

    def particle_trail(self):
        particle_direction = (self.heading - pi) + uniform(-0.47, 0.47)
        particle_vector = (-cos(particle_direction), -sin(particle_direction))
        globs.renderer.add_trail_particle((self.x, self.y), particle_vector)
