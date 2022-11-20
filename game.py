import random

from globals import *
from hole import Hole


# Singleton class
class Game:
    instance_ = None

    def __init__(self):
        self.bg_color = BACKGROUND_COLOR
        self.sprite_group = {}
        self.lives = 6
        self.score = 0
        self.line_list = []
        self.hole_list = []

    # spawn new hole
    def spawn_hole(self, x, y, speed, grp):
        hole = Hole(x, y)
        hole.vel = speed
        grp.add(hole)
        self.hole_list.append(hole)
        return hole

    # spawn new hole at random location
    def spawn_random_hole(self, grp):
        if len(self.hole_list) < 8:
            x = random.randint(L_SCREEN_EDGE, R_SCREEN_EDGE)
            y = self.line_list[random.randint(0, 7)].rect.y
            hole_sign = random.randint(0, 1)
            if hole_sign == 0:
                speed = HOLE_SPEED
            else:
                speed = -HOLE_SPEED
            self.spawn_hole(x, y, speed, grp)

    @staticmethod
    def instance():
        if Game.instance_ is None:
            Game.instance_ = Game()
        return Game.instance_

    @staticmethod
    def destroy():
        Game.instance_ = None
