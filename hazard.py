import random
import game_objects
import pygame.image
import game
from globals import *

hazards_names = ['octopus', 'train', 'ray', 'farmer', 'aeroplane', 'bus', 'dinosaur', 'witch', 'axe', 'snake']
hazards_color = [COLOR_BASIC_BLUE, COLOR_BASIC_GREEN, COLOR_BRIGHT_MAGENTA, COLOR_BASIC_YELLOW, COLOR_BASIC_BLACK,
                 COLOR_BASIC_RED]


# spawn a random hazard at random x coordinate
def spawn_hazard(grp):
    # 0 <= r < len(hazards_names)
    r = random.randrange(0, len(hazards_names))
    hazard = Hazard(hazards_names[r], len(game.Game.instance().hazard_list))

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


class Hazard(game_objects.ZSprite):
    def __init__(self, hazard_name, hazard):
        super().__init__()
        frame1 = pygame.image.load(f'img/enemies/{hazard_name}/{hazard_name}1.png')
        frame2 = pygame.image.load(f'img/enemies/{hazard_name}/{hazard_name}2.png')
        frame3 = pygame.image.load(f'img/enemies/{hazard_name}/{hazard_name}3.png')
        frame4 = pygame.image.load(f'img/enemies/{hazard_name}/{hazard_name}4.png')

        color_image = pygame.Surface(frame1.get_size()).convert_alpha(frame1)
        color_image.fill(hazards_color[hazard % 6])

        frame1.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        frame2.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        frame3.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        frame4.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        frame1 = pygame.transform.scale(frame1, (SCALED_HAZARD_SIZE[0], SCALED_HAZARD_SIZE[1]))
        frame2 = pygame.transform.scale(frame2, (SCALED_HAZARD_SIZE[0], SCALED_HAZARD_SIZE[1]))
        frame3 = pygame.transform.scale(frame3, (SCALED_HAZARD_SIZE[0], SCALED_HAZARD_SIZE[1]))
        frame4 = pygame.transform.scale(frame4, (SCALED_HAZARD_SIZE[0], SCALED_HAZARD_SIZE[1]))

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
        if self.x > SCALED_R_SCREEN_EDGE or self.x <= -SCALED_GAP_WIDTH + SCALED_L_SCREEN_EDGE:
            self.wrap()
        super().update(*args, **kwargs)

    def wrap(self):
        if self.x <= -SCALED_L_SCREEN_EDGE:
            self.x = SCALED_R_SCREEN_EDGE
            self.y = self.y - SCALED_LINES_DISTANCE
            if self.y < -(16 * SCALE_FACTOR_Y):
                self.y = game.Game.instance().line_list[7].rect.y - (16 * SCALE_FACTOR_Y)
