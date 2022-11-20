import random

from globals import *
from hole import Hole


# crea una nuova buca
def spawn_hole(x, y, speed, grp):
    hole = Hole(x, y)
    hole.vel = speed
    grp.add(hole)
    hole_list.append(hole)
    return hole


def spawn_random_hole(grp):
    if len(hole_list) < 8:
        x = random.randint(0, 799)
        y = line_list[random.randint(0, 7)].rect.y
        hole_sign = random.randint(0, 1)
        if hole_sign == 0:
            speed = HOLES_SPEED
        else:
            speed = -HOLES_SPEED
        spawn_hole(x, y, speed, grp)


# Singleton class
class Game:
    instance = None

    def __init__(self):
        self.background_color = BACKGROUND_COLOR
        self.group = None
        self.lives = 6
        self.score = 0

    def set_lives(self, lives):
        self.lives = lives

    def get_lives(self):
        return self.lives

    def set_bg_color(self, color):
        self.background_color = color

    def get_bg_color(self):
        return self.background_color

    def set_group(self, grp):
        self.group = grp

    def get_group(self):
        return self.group

    @staticmethod
    def get_instance():
        if Game.instance is None:
            Game.instance = Game()
        return Game.instance

    @staticmethod
    def destroy_instance():
        Game.instance = None
