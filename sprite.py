import pygame as pg
import colors
from functools import cache
from math import degrees
import globs


class Sprite(pg.sprite.Sprite):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.original_image = pg.image.load(f"{globs.ASSET_PATH}bezi2.png").convert()
        self.original_image.set_colorkey((69, 69, 69))
        self.original_image = pg.transform.rotate(self.original_image, 270)
        # self.original_image.fill(colors.BLACK)
        # pg.draw.rect(self.original_image, colors.WHITE, (0,0,50,50))
        self.rect = self.original_image.get_rect()
        self.image = self.original_image

    @cache
    def rotate_image(self, radians_rotate: float) -> None:
        self.image = pg.transform.rotate(self.original_image, -degrees(radians_rotate))
