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

import random
import pygame
import game
from globals import *

DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF
# DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF|pygame.FULLSCREEN


# ------------------------------------inizio main --------------------------------------------
random.seed()
pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DISPLAY_MODE_FLAGS, vsync=1)
pygame.display.set_caption('Jumping Jack')

# load asset
game.Game.instance().load_resources()
# run the game
game.Game.instance().run()

game.Game.destroy()
pygame.mixer.quit()
pygame.font.quit()
pygame.quit()
