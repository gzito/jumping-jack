from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from globals import *


class Hole(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS))
        self.image.fill(BACKGROUND_COLOR)
        self.rect = Rect(x, y, SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS)
        self.vel = 0

    def update(self, *args, **kwargs):
        self.rect.x += self.vel
        if self.rect.x > SCALED_R_SCREEN_EDGE or self.rect.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.wrap()

        self.rect.update(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def wrap(self):
        if self.rect.x > SCALED_R_SCREEN_EDGE:
            self.rect.x = SCALED_L_SCREEN_EDGE
            self.rect.y = self.rect.y + SCALED_LINES_DISTANCE
            if self.rect.y > 7 * SCALED_LINES_DISTANCE:
                self.rect.y = 0
        elif self.rect.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.rect.x = SCALED_R_SCREEN_EDGE
            self.rect.y = self.rect.y - SCALED_LINES_DISTANCE
            if self.rect.y < 0:
                self.rect.y = 7 * SCALED_LINES_DISTANCE
