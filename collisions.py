import pygame as pg
import game_math as gm
import shapes
import globs


class Collider:
    def do_player_collisions(self, points: list) -> dict:
        level = globs.level_handler.load_level()
        death = False
        winning = False
        for point in points:
            if self.do_player_killer_collision(level["killers"], pg.Vector2(point)):
                death = True
                break
            if self.collide_rect(point, level["finish"]):
                winning = True
                break

        return {"death": death, "winning": winning}

    def do_player_killer_collision(self, killers: dict, point: pg.Vector2) -> bool:
        circle_killers = killers["circles"]
        rect_killers = killers["rects"]
        for circle in circle_killers:
            if self.collide_circle(pg.Vector2(point), circle):
                return True
        for rect in rect_killers:
            if self.collide_rect(point, rect):
                return True
        return False

    def collide_circle(self, point: pg.Vector2, circle: shapes.Circle) -> bool:
        return gm.pythag((point.x - circle[0]), (point.y - circle[1])) < circle[2]

    def collide_rect(self, point: pg.Vector2, rect: shapes.Rect) -> bool:
        pg_rect = pg.Rect(rect[0], rect[1], rect[2], rect[3])
        return pg_rect.collidepoint(point[0], point[1])
