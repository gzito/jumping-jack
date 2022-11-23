import random
import game
import pygame
import game_objects
from globals import *


# spawn new hole
def spawn_hole(x, y, speed, grp):
    hole = Hole(x, y)
    hole.speed = speed
    grp.add(hole)
    game.Game.instance().hole_list.append(hole)
    return hole


# spawn new hole at random location
def spawn_random_hole(grp):
    if len(game.Game.instance().hole_list) < 8:
        x = random.randint(SCALED_L_SCREEN_EDGE, SCALED_R_SCREEN_EDGE)
        y = game.Game.instance().line_list[random.randint(0, 7)].rect.y
        hole_sign = random.randint(0, 1)
        if hole_sign == 0:
            speed = SCALED_HOLE_SPEED
        else:
            speed = -SCALED_HOLE_SPEED
        spawn_hole(x, y, speed, grp)


class Hole(game_objects.ZSprite):
    # static member
    color_dict_ = {}

    def __init__(self, x, y):
        super().__init__()

        if BACKGROUND_COLOR not in Hole.color_dict_:
            surface = pygame.surface.Surface((SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(BACKGROUND_COLOR)
            Hole.color_dict_[BACKGROUND_COLOR] = surface

        if FLASH_COLOR not in Hole.color_dict_:
            surface = pygame.surface.Surface((SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(FLASH_COLOR)
            Hole.color_dict_[FLASH_COLOR] = surface

        self.current_surface = Hole.color_dict_[BACKGROUND_COLOR]
        self.surface_switched = False

        self.image = Hole.color_dict_[BACKGROUND_COLOR]
        self.rect = pygame.rect.Rect(x, y, SCALED_HOLE_WIDTH, SCALED_LINE_THICKNESS)
        self.speed = 0.0

        self.set_position(x, y)

    def update(self, *args, **kwargs):
        self.set_x(self.x + self.speed)
        if self.x > SCALED_R_SCREEN_EDGE or self.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.wrap()

        if self.surface_switched:
            self.image = self.current_surface
            self.surface_switched = False

        super().update(*args, **kwargs)

    def wrap(self):
        if self.x > SCALED_R_SCREEN_EDGE:
            self.x = SCALED_L_SCREEN_EDGE
            self.y = self.y + SCALED_LINES_DISTANCE
            if self.y > 7 * SCALED_LINES_DISTANCE:
                self.y = 0
        elif self.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.x = SCALED_R_SCREEN_EDGE
            self.y = self.y - SCALED_LINES_DISTANCE
            if self.y < 0:
                self.y = 7 * SCALED_LINES_DISTANCE

    def switch_surface(self, color):
        self.current_surface = Hole.color_dict_[color]
        self.surface_switched = True
