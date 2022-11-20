import pygame
from globals import *


class Line(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((LINE_WIDTH, LINE_THICKNESS))
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x, y, LINE_WIDTH, LINE_THICKNESS)
        self.rect.x = x
        self.rect.y = y
        self.rect.right = x + LINE_WIDTH
        self.rect.bottom = y + LINE_THICKNESS
