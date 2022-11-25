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
import game_objects
import pygame.image
import game
from globals import *


class Hazard(game_objects.ZSprite):
    hazards_names = ['octopus', 'train', 'ray', 'farmer', 'aeroplane', 'bus', 'dinosaur', 'witch', 'axe', 'snake']
    hazards_color = [COLOR_BASIC_BLUE, COLOR_BASIC_GREEN, COLOR_BRIGHT_MAGENTA, COLOR_BASIC_YELLOW, COLOR_BASIC_BLACK,
                     COLOR_BASIC_RED]

    def __init__(self, hazard_name, hazard):
        super().__init__()

        frame = []

        for num in range(1, 5):
            frame.append(game.Game.instance().get_surface(f'{hazard_name}{num}').copy())

        color_image = pygame.Surface(frame[0].get_size()).convert_alpha()
        color_image.fill(Hazard.hazards_color[hazard % 6])

        for num in range(0, 4):
            frame[num].blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            frame[num] = pygame.transform.scale(frame[num], (SCALED_HAZARD_SIZE[0], SCALED_HAZARD_SIZE[1]))

        default_anim = game_objects.Animation2D(True)
        default_anim.loop = True
        default_anim.speed = 1
        for num in range(0, 4):
            default_anim.add_frame(game_objects.AnimFrame2D(frame[num], 0.10))

        self.add_animation("default", default_anim)
        self.set_animation(default_anim)

        self.speed = 0

    def update(self, *args, **kwargs):
        self.move(self.speed)
        if self.x > SCALED_R_SCREEN_EDGE or self.x <= -SCALED_GAP_WIDTH + SCALED_L_SCREEN_EDGE:
            self.wrap()
        super().update(*args, **kwargs)

    def wrap(self):
        if self.x <= -SCALED_L_SCREEN_EDGE:
            self.x = SCALED_R_SCREEN_EDGE
            self.y = self.y - SCALED_LINES_DISTANCE
            if self.y < -(16 * SCALE_FACTOR_Y):
                self.y = game.Game.instance().line_list[7].rect.y - (16 * SCALE_FACTOR_Y)

    # spawn a random hazard at random x coordinate
    @staticmethod
    def spawn_hazard(grp):
        # 0 <= r < len(Hazard.hazards_names)
        r = random.randrange(0, len(Hazard.hazards_names))
        hazard = Hazard(Hazard.hazards_names[r], len(game.Game.instance().hazard_list))

        while True:
            x = random.randint(SCALED_L_SCREEN_EDGE, SCALED_R_SCREEN_EDGE)
            y = game.Game.instance().line_list[random.randint(1, 6)].rect.y - (16 * SCALE_FACTOR_Y)
            hazard.set_position(x, y)
            if pygame.sprite.spritecollideany(hazard, game.Game.instance().sprite_group[GROUP_HAZARDS]) is None and \
                    pygame.sprite.spritecollideany(hazard, game.Game.instance().sprite_group[GROUP_PLAYER]) is None:
                break

        hazard.speed = -SCALED_HAZARD_SPEED

        grp.add(hazard)
        game.Game.instance().hazard_list.append(hazard)
        return hazard
