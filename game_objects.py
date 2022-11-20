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
        self.animation = None  # animazione corrente
        self.direction = 0  # direzione (1-destra, -1-sinistra, 0-fermo)
        self.animations = {}  # dizionario delle animazioni
        self.x = 0  # posizione sprite x
        self.y = 0  # posizione sprite y

    def set_hotspot(self, hx, hy):
        self.hotspot.x = hx
        self.hotspot.y = hy

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.move_ip(x - self.hotspot.x, y - self.hotspot.y)

    def get_position(self):
        return Point(self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x
        self.rect.update(self.x, self.y, self.rect.width, self.rect.height)

    def set_y(self, y):
        self.y = y
        self.rect.update(self.x, self.y, self.rect.width, self.rect.height)

    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.rect.move_ip(dx - self.hotspot.x, dy - self.hotspot.y)

    def set_frame(self, frame):
        self.image = frame.image
        self.rect = Rect(0, 0, frame.image.get_width(), frame.image.get_height())

    # imposta una nuova animazione per lo sprite
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

    def add_animation(self, name, animation):
        self.animations[name] = animation

    def draw_debug_rect(self):
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color(0, 0, 0), self.rect, 2)
        pygame.draw.line(pygame.display.get_surface(), pygame.Color(255, 0, 0), (self.rect.x - 10, 513.6),
                         (self.rect.x - 5, 513.6))


# frame dell'animazione
class AnimFrame2D:
    def __init__(self, sprite_frame, frame_duration):
        self.sprite_frame = sprite_frame  # immagine
        self.duration = frame_duration  # durata dell'immagine in secondi
        self.flip_x = False  # flip su x
        self.flip_y = False  # flip su y
        self.partial_time = 0.0  # somma del tempo dei frame già visualizzati più quello attuale


class Animation2D:
    def __init__(self, autostart=False):
        self.frames = []  # lista dei frame
        self.total_duration = 0.0  # durata totale dell'animazione in secondi
        self.loop = False  # indica se l'animazione è in loop
        self.flip_all_x = False
        self.flip_all_y = False
        self.speed = 1.0  # moltiplicatore velocità animazione
        self.started = autostart  # flag per sapere se l'animazione è iniziata
        self.current_time = 0.0  # tempo attuale dell'animazione
        self.current_frame_index = 0  # indice della lista rispettivo al frame visualizzato

    def add_frame(self, frame):
        self.frames.append(frame)  # aggiunge un frame alla lista
        self.total_duration += frame.duration  # aggiunge la durata del frame attuale alla durata dell'animazione
        #        self.frames[len(self.frames) - 1].partial_time = self.total_duration
        frame.partial_time = self.total_duration

    def update(self, delta_time):
        if self.started:
            # calcola il tempo
            self.current_time += delta_time * self.speed
            elapsed = self.current_time
            time_count = 0.0

            # gestisce il loop
            if self.loop and elapsed > self.total_duration:
                elapsed = elapsed % self.total_duration

            # calcola il fotogramma attuale basato sul tempo
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
