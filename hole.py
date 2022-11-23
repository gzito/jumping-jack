from pygame.rect import Rect
from pygame.surface import Surface

from game_objects import ZSprite
from globals import *


class Hole(ZSprite):
    # static member
    color_dict_ = {}

    def __init__(self, x, y):
        super().__init__()

        if BACKGROUND_COLOR not in Hole.color_dict_:
            surface = Surface((SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(BACKGROUND_COLOR)
            Hole.color_dict_[BACKGROUND_COLOR] = surface

        if FLASH_COLOR not in Hole.color_dict_:
            surface = Surface((SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(FLASH_COLOR)
            Hole.color_dict_[FLASH_COLOR] = surface

        self.current_surface = Hole.color_dict_[BACKGROUND_COLOR]
        self.surface_switched = False

        self.image = Hole.color_dict_[BACKGROUND_COLOR]
        self.rect = Rect(x, y, SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS)
        self.vel = 0.0

    def update(self, *args, **kwargs):
        self.set_x(self.x + self.vel)
        if self.x > SCALED_R_SCREEN_EDGE or self.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.wrap()

        if self.surface_switched:
            self.image = self.current_surface
            self.surface_switched = False

        super().update(*args, **kwargs)

    def wrap(self):
        if self.x > SCALED_R_SCREEN_EDGE:
            self.x = SCALED_L_SCREEN_EDGE
            self.y = self.y + SCALED_LINES_DISTANCE
            if self.y > 7 * SCALED_LINES_DISTANCE:
                self.y = 0
        elif self.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.x = SCALED_R_SCREEN_EDGE
            self.y = self.y - SCALED_LINES_DISTANCE
            if self.y < 0:
                self.y = 7 * SCALED_LINES_DISTANCE

    def switch_surface(self, color):
        self.current_surface = Hole.color_dict_[color]
        self.surface_switched = True
