import pygame.display
from pygame.time import Clock

from game import Game
from hole import Hole


class ScreenFlash:
    def __init__(self, orig_color, flash_color, duration_ms, times):
        self.colors = (orig_color, flash_color)
        self.next_color_idx = 0
        self.duration_ms = duration_ms
        self.counter = 0
        self.times = times
        self.clock = None
        self.start_ms = 0
        self.current_ms = 0
        self.is_enabled = False

    def start(self):
        self.clock = Clock()
        self.start_ms = 0
        self.current_ms = 0
        self.is_enabled = True
        self.counter = 0
        self.next_color_idx = 1
        Game.instance().set_bg_color(self.colors[self.next_color_idx])

    def update(self):
        if self.is_enabled:
            self.current_ms += self.clock.tick()
            if self.current_ms - self.start_ms >= self.duration_ms:
                self.start_ms = self.current_ms
                self.next_color_idx += 1
                if self.next_color_idx > 1:
                    self.next_color_idx = 0
                Game.instance().set_bg_color(self.colors[self.next_color_idx])
                self.counter = self.counter + 1
                if self.counter >= self.times:
                    self.stop()

    def stop(self):
        Game.instance().set_bg_color(self.colors[0])
        self.is_enabled = False
