import random
import pygame
from pygame.font import Font

from globals import *
from hole import Hole
from line import Line


# Singleton class
class Game:
    instance_ = None

    def __init__(self):
        self.bg_color = BACKGROUND_COLOR
        self.font = None
        self.sprite_group = {}
        self.lives = LIVES
        self.score = 0
        self.level = 1
        self.line_list = []
        self.hole_list = []
        self.life_list = []
        self.state = PlayingState()

        # sprites groups
        self.sprite_group[GROUP_BCKGRND] = pygame.sprite.Group()
        self.sprite_group[GROUP_HUD] = pygame.sprite.Group()
        self.sprite_group[GROUP_ENEMIES] = pygame.sprite.Group()
        self.sprite_group[GROUP_PLAYER] = pygame.sprite.Group()

        self.font = Font('fonts/zxspectr.ttf', 8)

    def set_bg_color(self, color):
        self.bg_color = color
        for hole in self.hole_list:
            hole.switch_surface(color)

    def create_floors(self):
        for i in range(8):
            line = Line(i)
            self.line_list.append(line)
            self.sprite_group[GROUP_BCKGRND].add(line)

    # spawn new hole
    def spawn_hole(self, x, y, speed, grp):
        hole = Hole(x, y)
        hole.speed = speed
        grp.add(hole)
        self.hole_list.append(hole)
        return hole

    # spawn new hole at random location
    def spawn_random_hole(self, grp):
        if len(self.hole_list) < 8:
            x = random.randint(SCALED_L_SCREEN_EDGE, SCALED_R_SCREEN_EDGE)
            y = self.line_list[random.randint(0, 7)].rect.y
            hole_sign = random.randint(0, 1)
            if hole_sign == 0:
                speed = SCALED_HOLE_SPEED
            else:
                speed = -SCALED_HOLE_SPEED
            self.spawn_hole(x, y, speed, grp)

    def decrement_lives(self):
        self.lives -= 1
        last_live = self.life_list[-1]
        del self.life_list[-1]
        self.sprite_group[GROUP_HUD].remove(last_live)

    def level_up(self):
        pass

    @staticmethod
    def instance():
        if Game.instance_ is None:
            Game.instance_ = Game()
        return Game.instance_

    @staticmethod
    def destroy():
        Game.instance_ = None


class GameState:
    def handle_input(self):
        pass

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass


class PlayingState(GameState):
    def __init__(self):
        super().__init__()


class LevelUpState(GameState):
    def __init__(self):
        super().__init__()

    def enter(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass


class GameOverState(GameState):
    def __init__(self):
        super().__init__()


