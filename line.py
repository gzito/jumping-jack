import pygame
from globals import *


class Line(pygame.sprite.Sprite):
    def __init__(self, i):
        super().__init__()
        x = SCALED_L_SCREEN_EDGE
        y = i * SCALED_LINES_DISTANCE
        print(f'linea {i}: {i * SCALED_LINES_DISTANCE}')
        self.image = pygame.Surface((SCALED_LINE_WIDTH, SCALED_LINE_THICKNESS))
        self.image.fill(LINE_COLOR)
        self.rect = pygame.Rect(x, y, SCALED_LINE_WIDTH, SCALED_LINE_THICKNESS)
