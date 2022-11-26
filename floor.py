"""
MIT License

Copyright (c) 2022 Giovanni Zito

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pygame
from globals import *


class Floor(pygame.sprite.Sprite):
    def __init__(self, i):
        super().__init__()
        x = SCALED_SCREEN_OFFSET_X
        y = SCALED_SCREEN_OFFSET_Y + (i * SCALED_FLOOR_DISTANCE)
        # print(f'floor {i}: {i * SCALED_FLOOR_DISTANCE}')
        self.image = pygame.Surface((SCALED_FLOOR_WIDTH, SCALED_FLOOR_THICKNESS))
        self.image.fill(FLOOR_COLOR)
        self.rect = pygame.Rect(x, y, SCALED_FLOOR_WIDTH, SCALED_FLOOR_THICKNESS)
