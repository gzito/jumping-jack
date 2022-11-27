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

import pygame.gfxdraw
import pygame.time
import game
from globals import *


class ColorFlash:
    # the last color in colors_list have to be the orginal color to be restored at the end of color flash
    def __init__(self, colors_list, duration_ms, times, start_delay_ms=0):
        self.__colors = colors_list
        self.__next_color_idx = 0
        self.__duration_ms = duration_ms
        self.__counter = 0
        self.__times = times
        self.__clock = None
        self.__start_ms = 0
        self.__current_ms = 0
        self.__start_delay_ms = start_delay_ms
        self.__is_enabled = False

    def start(self):
        self.__clock = pygame.time.Clock()
        self.__start_ms = 0
        self.__current_ms = 0
        self.__is_enabled = True
        self.__counter = 0
        self.__next_color_idx = 0

    def update(self):
        if self.__is_enabled:
            self.__current_ms += self.__clock.tick()
            if self.__current_ms <= self.__start_delay_ms:
                return
            if self.__current_ms - self.__start_ms >= self.__duration_ms:
                self.__start_ms = self.__current_ms
                self.__next_color_idx += 1
                if self.__next_color_idx >= len(self.__colors):
                    self.__counter += 1
                    if self.__counter < self.__times:
                        self.__next_color_idx = 0
                    else:
                        self.__next_color_idx = len(self.__colors) - 1
                if self.__counter >= self.__times:
                    self.stop()

    def stop(self):
        self.__is_enabled = False

    def is_enabled(self):
        return self.__is_enabled and self.__current_ms >= self.__start_delay_ms

    def get_current_color(self):
        retval = None
        if self.__is_enabled:
            retval = self.__colors[self.__next_color_idx]
        return retval


class MulticolorBorderFlash:
    def __init__(self, line_size):
        self.__color_list = [COLOR_BASIC_BLACK,
                             COLOR_BASIC_BLUE,
                             COLOR_BASIC_RED,
                             COLOR_BASIC_MAGENTA,
                             COLOR_BASIC_GREEN,
                             COLOR_BASIC_CYAN,
                             COLOR_BASIC_YELLOW,
                             COLOR_BASIC_WHITE,
                             COLOR_BRIGHT_BLACK,
                             COLOR_BRIGHT_BLUE,
                             COLOR_BRIGHT_RED,
                             COLOR_BRIGHT_MAGENTA,
                             COLOR_BRIGHT_GREEN,
                             COLOR_BRIGHT_CYAN,
                             COLOR_BRIGHT_YELLOW,
                             COLOR_BRIGHT_WHITE]

        self.__color_idx = 0
        self.__line_size = line_size

    def update(self):
        c = self.__color_idx
        y = 0
        while y < round(SCALED_SCREEN_OFFSET_Y):
            pygame.gfxdraw.box(game.Game.instance().screen,
                               (0, y, DISPLAY_WIDTH, zxh2h(self.__line_size)),
                               self.__color_list[c])
            c = clamp(c, 1, 0, len(self.__color_list))
            y += zxh2h(self.__line_size)

        while y < round(SCALED_BOTTOM_BORDER_Y):
            pygame.gfxdraw.box(game.Game.instance().screen,
                               (0, y, zxw2w(ZX_LEFT_BORDER_WIDTH), zxh2h(self.__line_size)),
                               self.__color_list[c])
            pygame.gfxdraw.box(game.Game.instance().screen,
                               (SCALED_RIGHT_BORDER_X, y, zxw2w(ZX_RIGHT_BORDER_WIDTH), zxh2h(self.__line_size)),
                               self.__color_list[c])
            c = clamp(c, 1, 0, len(self.__color_list))
            y += zxh2h(self.__line_size)

        while y < round(DISPLAY_HEIGHT):
            pygame.gfxdraw.box(game.Game.instance().screen,
                               (0, y, DISPLAY_WIDTH, zxh2h(self.__line_size)),
                               self.__color_list[c])
            c = clamp(c, 1, 0, len(self.__color_list))
            y += zxh2h(self.__line_size)

        self.__color_idx = clamp(c, 2, 0, len(self.__color_list))
