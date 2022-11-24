import random
import game_objects
import pygame.image
import game
from globals import *

enemies_names = ['octopus', 'train', 'ray', 'farmer', 'aeroplane', 'bus', 'dinosaur', 'witch', 'axe', 'snake']
hazards_color = [COLOR_BASIC_BLUE, COLOR_BASIC_BLUE, COLOR_BRIGHT_MAGENTA, COLOR_BASIC_YELLOW, COLOR_BASIC_BLACK,
                 COLOR_BASIC_RED]


def spawn_enemy(x, y, speed, grp):
    # 0 <= r < len(enemies_names)
    r = random.randrange(0, len(enemies_names))
    enemy = Enemy(enemies_names[r], len(game.Game.instance().enemy_list))
    enemy.set_position(x, y)
    enemy.speed = speed
    grp.add(enemy)
    game.Game.instance().enemy_list.append(enemy)
    return enemy


def spawn_random_enemy(grp):
    if len(game.Game.instance().enemy_list) < MAX_HAZARDS:
        x = random.randint(SCALED_L_SCREEN_EDGE, SCALED_R_SCREEN_EDGE)
        y = game.Game.instance().line_list[random.randint(1, 6)].rect.y - (16 * SCALE_FACTOR_Y)
        speed = -SCALED_ENEMY_SPEED
        spawn_enemy(x, y, speed, grp)


class Enemy(game_objects.ZSprite):
    def __init__(self, enemy_name, hazard):
        super().__init__()
        frame1 = pygame.image.load(f'img/enemies/{enemy_name}/{enemy_name}1.png')
        frame2 = pygame.image.load(f'img/enemies/{enemy_name}/{enemy_name}2.png')
        frame3 = pygame.image.load(f'img/enemies/{enemy_name}/{enemy_name}3.png')
        frame4 = pygame.image.load(f'img/enemies/{enemy_name}/{enemy_name}4.png')

        color_image = pygame.Surface(frame1.get_size()).convert_alpha(frame1)
        color_image.fill(hazards_color[hazard % 6])

        frame1.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        frame2.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        frame3.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        frame4.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        frame1 = pygame.transform.scale(frame1, (SCALED_ENEMY_SIZE[0], SCALED_ENEMY_SIZE[1]))
        frame2 = pygame.transform.scale(frame2, (SCALED_ENEMY_SIZE[0], SCALED_ENEMY_SIZE[1]))
        frame3 = pygame.transform.scale(frame3, (SCALED_ENEMY_SIZE[0], SCALED_ENEMY_SIZE[1]))
        frame4 = pygame.transform.scale(frame4, (SCALED_ENEMY_SIZE[0], SCALED_ENEMY_SIZE[1]))

        default_anim = game_objects.Animation2D(True)
        default_anim.loop = True
        default_anim.speed = 1
        default_anim.add_frame(game_objects.AnimFrame2D(frame1, 0.10))
        default_anim.add_frame(game_objects.AnimFrame2D(frame2, 0.10))
        default_anim.add_frame(game_objects.AnimFrame2D(frame3, 0.10))
        default_anim.add_frame(game_objects.AnimFrame2D(frame4, 0.10))

        self.add_animation("default", default_anim)
        self.set_animation(default_anim)

        self.speed = 0

    def update(self, *args, **kwargs):
        self.move(self.speed)
        if self.x > SCALED_R_SCREEN_EDGE or self.x <= -SCALED_HOLE_WIDTH + SCALED_L_SCREEN_EDGE:
            self.wrap()
        super().update(*args, **kwargs)

    def wrap(self):
        if self.x <= -SCALED_L_SCREEN_EDGE:
            self.x = SCALED_R_SCREEN_EDGE
            self.y = self.y - SCALED_LINES_DISTANCE
            if self.y < -(16 * SCALE_FACTOR_Y):
                self.y = game.Game.instance().line_list[7].rect.y - (16 * SCALE_FACTOR_Y)
