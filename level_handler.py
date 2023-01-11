import json
import globs
import os
import game_math as gm
from pygame import Vector2


class LevelHandler:
    blank_dict = {
    "starting_pos":[100,100,0],
    "killers":{
        "circles":[],
        "rects":[]
        },
    "finish":[900,900,50,50]
    }
    level_path = "levels/"
    current_level: int = 0
    level: dict

    def get_level_name(self, level: int) -> str:
        return f"{self.level_path}/level{level}.json"

    def load_level(self, level: int = None):
        if level == None:
            level = self.current_level
        with open(self.get_level_name(level)) as f:
            dict = json.load(f)
        self.level = dict
        return dict

    def write_level(self, level: int = None):
        if level == None:
            level = self.current_level
        with open(self.get_level_name(level), "w") as f:
            f.write(json.dumps(self.level))

    def get_starting_pos(self):
        if self.level is None:
            raise Exception("no level loaded")
        return self.level["starting_pos"]

    def advance_level(self):
        self.current_level += 1
        try:
            self.load_level(self.current_level)
        except Exception:
            print("Next level does not exist; fix me")
        globs.renderer.render_level(self.level)

    def add_rect_killer(self, loc1, loc2):
        rect = self.make_rect(loc1, loc2)
        self.level["killers"]["rects"].append(rect)

    def add_circle_killer(self, loc1, loc2):
        circle = self.make_circle(loc1, loc2)
        self.level["killers"]["circles"].append(circle)

    def make_rect(self, loc1, loc2):
        x = min(loc1[0], loc2[0])
        y = min(loc1[1], loc2[1])
        width = abs(loc1[0] - loc2[0])
        height = abs(loc1[1] - loc2[1])
        rect = x, y, width, height
        return rect

    def make_circle(self, loc1, loc2):
        x, y = loc1
        radius = gm.len_linear_2d(Vector2(loc1), Vector2(loc2))
        return x, y, radius

    def demolish(self, location):
        for i, circle in enumerate(self.level["killers"]["circles"]):
            x, y, r = circle
            if gm.len_linear_2d(Vector2(location), Vector2(x, y)) < r:
                self.level["killers"]["circles"].pop(i)
                return

        for i, rect in enumerate(self.level["killers"]["rects"]):
            if globs.collider.collide_rect(location, rect):
                self.level["killers"]["rects"].pop(i)
                return

    def set_start(self, location, heading=0):
        x, y = location
        self.level["starting_pos"] = x, y, heading

    def make_file(self, num:int):
        self.current_level = num
        self.level = self.blank_dict
        self.write_level()