import pygame
from globals import *


class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((HOLE_WIDTH, 6))
        self.image.fill(BACKGROUND_COLOR)
        self.rect = pygame.Rect(x, y, HOLE_WIDTH, 6)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = HOLE_WIDTH
        self.rect.bottom = y + 6
        self.vel = 0

    def update(self, *args, **kwargs):
        self.rect.x += self.vel
        if self.rect.x > R_SCREEN_EDGE or self.rect.x <= -HOLE_WIDTH + L_SCREEN_EDGE:
            self.wrap()

        self.rect.update(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def wrap(self):
        if self.rect.x > R_SCREEN_EDGE:
            self.rect.x = L_SCREEN_EDGE
            self.rect.y = self.rect.y + LINES_DISTANCE
            if self.rect.y > 490:
                self.rect.y = 70
        elif self.rect.x <= -HOLE_WIDTH + L_SCREEN_EDGE:
            self.rect.x = R_SCREEN_EDGE
            self.rect.y = self.rect.y - LINES_DISTANCE
            if self.rect.y < 70:
                self.rect.y = 490
