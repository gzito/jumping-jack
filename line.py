import pygame
from globals import *


class Line(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((LINEA_WIDTH, LINEA_SPESSORE))
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x, y, LINEA_WIDTH, LINEA_SPESSORE)
        self.rect.x = x
        self.rect.y = y
        self.rect.right = x + LINEA_WIDTH
        self.rect.bottom = y + LINEA_SPESSORE
