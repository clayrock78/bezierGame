import pygame as pg
import fonts
import colors
import globs


class LETexter:
    font = fonts.FPS_FONT

    def notify(self, text):
        text = self.font.render(text, True, colors.PURPLE)
        text_rect = text.get_rect(top=0, left=0)
        globs.renderer.text_layer.blit(text, text_rect)
