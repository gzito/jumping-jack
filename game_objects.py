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

import pygame
from pygame.rect import Rect


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class ZSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.hotspot = Point()  # hotspot
        self.animation = None  # current animation
        self.direction = 0  # direction (1-right, -1-left, 0-halted)
        self.animations = {}  # animations dictionary
        self.x = 0.0  # sprite x-location
        self.y = 0.0  # sprite y-location

    def set_hotspot(self, hx, hy):
        self.hotspot.x = hx
        self.hotspot.y = hy

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.update(self.x - self.hotspot.x, self.y - self.hotspot.y, self.rect.width, self.rect.height)

    def get_position(self):
        return Point(self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def move(self, dx=0.0, dy=0.0):
        self.x += dx
        self.y += dy

    def set_frame(self, frame):
        self.image = frame.image
        self.rect = Rect(0, 0, frame.image.get_width(), frame.image.get_height())

    # set a new animation for the sprite
    def set_animation(self, anim):
        if self.animation != anim:
            self.animation = anim
            self.animation.restart()
            self.image = self.animation.get_current_frame()
            self.rect = self.image.get_rect()
            self.set_position(self.x, self.y)

    def get_animation(self):
        return self.animation

    # args is delta_time
    def update(self, *args, **kwargs):
        if self.animation is not None:
            self.animation.update(args[0])
            self.image = self.animation.get_current_frame()
        self.rect.update(self.x, self.y, self.rect.width, self.rect.height)

    def add_animation(self, name, animation):
        self.animations[name] = animation

    def draw_debug_rect(self):
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color(0, 0, 0), self.rect, 2)
        pygame.draw.line(pygame.display.get_surface(), pygame.Color(255, 0, 0), (self.rect.x - 10, 513.6),
                         (self.rect.x - 5, 513.6))


# animation frame
class AnimFrame2D:
    def __init__(self, sprite_frame, frame_duration):
        self.sprite_frame = sprite_frame  # image
        self.duration = frame_duration  # in seconds
        self.flip_x = False  # flip on x
        self.flip_y = False  # flip on y
        self.partial_time = 0.0  # sum of the time of the frames already displayed plus the current one


class Animation2D:
    def __init__(self, autostart=False):
        self.frames = []  # frames list
        self.total_duration = 0.0  # total duration of the animation in seconds
        self.loop = False  # indicates if the animation is looping
        self.flip_all_x = False
        self.flip_all_y = False
        self.speed = 1.0  # animation speed multiplier
        self.started = autostart  # flag to know if the animation has started
        self.current_time = 0.0  # current time of the animation
        self.current_frame_index = 0  # index of the list corresponding to the displayed frame

    def add_frame(self, frame):
        self.frames.append(frame)  # adds a frame to the list
        self.total_duration += frame.duration  # adds the duration of the current frame to the duration of the animation
        #        self.frames[len(self.frames) - 1].partial_time = self.total_duration
        frame.partial_time = self.total_duration

    def update(self, delta_time):
        if self.started:
            # calculate the time
            self.current_time += delta_time * self.speed
            elapsed = self.current_time
            time_count = 0.0

            # handles the loop
            if self.loop and elapsed > self.total_duration:
                elapsed = elapsed % self.total_duration

            # calculates the current frame based on time
            self.current_frame_index = 0
            for self.current_frame_index in range(0, len(self.frames)):
                time_count = self.frames[self.current_frame_index].partial_time
                if elapsed < time_count:
                    break

    #            if self.current_frame_index >= len(self.frames):
    #                self.current_frame_index = len(self.frames) - 1

    def get_current_frame(self):
        frame = self.frames[self.current_frame_index]

        if self.flip_all_x:
            frame.flip_x = True

        if self.flip_all_y:
            frame.flip_y = True

        return frame.sprite_frame

    def is_ended(self):
        return self.current_time >= self.total_duration

    def restart(self):
        self.current_time = 0
