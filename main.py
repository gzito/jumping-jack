#
# URL of online zx spectrum emulator:
# http://torinak.com/qaop/games
# http://torinak.com/qaop#!jumpingjack
#
import random
import pygame

from globals import *
from game import Game

DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF
# DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF|pygame.FULLSCREEN


# ------------------------------------inizio main --------------------------------------------
random.seed()
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(RESOLUTION, DISPLAY_MODE_FLAGS, vsync=1)
pygame.display.set_caption('Jumping Jack')

Game.instance().run()

Game.destroy()
pygame.font.quit()
pygame.quit()
