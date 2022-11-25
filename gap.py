import random
import game
import pygame
import game_objects
from globals import *


# spawn new gap
def spawn_gap(x, y, speed, grp):
    gap = Gap(x, y)
    gap.speed = speed
    grp.add(gap)
    game.Game.instance().gap_list.append(gap)
    return gap


# spawn new gap at random location
def spawn_random_gap(grp):
    if len(game.Game.instance().gap_list) < MAX_GAPS:
        x = random.randint(SCALED_L_SCREEN_EDGE, SCALED_R_SCREEN_EDGE)
        y = game.Game.instance().line_list[random.randint(0, 7)].rect.y
        gap_dir = random.randint(0, 1)
        speed = SCALED_GAP_SPEED if gap_dir == 0 else -SCALED_GAP_SPEED
        spawn_gap(x, y, speed, grp)


class Gap(game_objects.ZSprite):
    # static member
    color_dict_ = {}

    def __init__(self, x, y):
        super().__init__()

        if BACKGROUND_COLOR not in Gap.color_dict_:
            surface = pygame.surface.Surface((SCALED_GAP_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(BACKGROUND_COLOR)
            Gap.color_dict_[BACKGROUND_COLOR] = surface

        if FLASH_COLOR_FLOOR_HIT not in Gap.color_dict_:
            surface = pygame.surface.Surface((SCALED_GAP_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(FLASH_COLOR_FLOOR_HIT)
            Gap.color_dict_[FLASH_COLOR_FLOOR_HIT] = surface

        if FLASH_COLOR_HAZARD_HIT not in Gap.color_dict_:
            surface = pygame.surface.Surface((SCALED_GAP_WIDTH, SCALED_LINE_THICKNESS))
            surface.fill(FLASH_COLOR_HAZARD_HIT)
            Gap.color_dict_[FLASH_COLOR_HAZARD_HIT] = surface

        self.current_surface = Gap.color_dict_[BACKGROUND_COLOR]
        self.surface_switched = False

        self.image = Gap.color_dict_[BACKGROUND_COLOR]
        self.rect = pygame.rect.Rect(x, y, SCALED_GAP_WIDTH, SCALED_LINE_THICKNESS)
        self.speed = 0.0

        self.set_position(x, y)

    def update(self, *args, **kwargs):
        self.set_x(self.x + self.speed)
        if self.x > SCALED_R_SCREEN_EDGE or self.x <= -SCALED_GAP_WIDTH + SCALED_L_SCREEN_EDGE:
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
        elif self.x <= -SCALED_GAP_WIDTH + SCALED_L_SCREEN_EDGE:
            self.x = SCALED_R_SCREEN_EDGE
            self.y = self.y - SCALED_LINES_DISTANCE
            if self.y < 0:
                self.y = 7 * SCALED_LINES_DISTANCE

    def switch_surface(self, color):
        self.current_surface = Gap.color_dict_[color]
        self.surface_switched = True
