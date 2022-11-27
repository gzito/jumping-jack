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
import pygame.gfxdraw

import hazard
import gap
import player
import floor
import color_flash
from globals import *


# Singleton class
class Game:
    instance_ = None

    def __init__(self):
        self.__bg_color = BACKGROUND_COLOR
        self.__border_color = BACKGROUND_COLOR
        self.__surfaces = {}
        self.__sfx = {}
        self.__state = None
        self.__new_state = None
        self.__is_border_draw_enabled = True

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        self.font = None

        self.floor_list = []
        self.gap_list = []
        self.hazard_list = []
        self.sprite_group = {GROUP_BCKGRND: pygame.sprite.Group(),
                             GROUP_HAZARDS: pygame.sprite.Group(),
                             GROUP_PLAYER: pygame.sprite.Group()}

        self.highscore = 0
        self.lives = LIVES
        self.score = 0
        self.hazards = 0

        self.set_initial_hazard_value()

    def restart(self):
        self.score = 0
        self.lives = LIVES
        self.set_initial_hazard_value()

    def set_initial_hazard_value(self):
        # level start from 0 (with no hazards) and runs until 20
        self.hazards = 0

    def border_draw_enable(self, enabled):
        self.__is_border_draw_enabled = enabled

    def is_border_draw_enabled(self):
        return self.__is_border_draw_enabled

    def load_resources(self):
        self.font = pygame.font.Font('fonts/zxspectr.ttf', int(8 * SCALE_FACTOR_X))

        # life
        life_frame = pygame.image.load(f'img/life.png')
        life_frame = pygame.transform.scale(life_frame, SCALED_LIFE_SIZE)
        self.add_surface('life', life_frame)

        # player
        for num in range(1, 4):
            frame = pygame.image.load(f'img/player/idle{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            self.add_surface(f'idle{num}', frame)

        for num in range(1, 5):
            frame = pygame.image.load(f'img/player/walk{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            self.add_surface(f'walk_right{num}', frame)
            frame = pygame.transform.flip(frame, True, False)
            self.add_surface(f'walk_left{num}', frame)

        for num in range(1, 4):
            frame = pygame.image.load(f'img/player/jump{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            self.add_surface(f'jump{num}', frame)

        for num in range(1, 7):
            frame = pygame.image.load(f'img/player/stunned{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            self.add_surface(f'stunned{num}', frame)

        # hazards
        for hazard_name in hazard.Hazard.hazards_names:
            for num in range(1, 5):
                frame = pygame.image.load(f'img/enemies/{hazard_name}/{hazard_name}{num}.png')
                self.add_surface(f'{hazard_name}{num}', frame)

        # sfx
        self.add_sfx('stand', pygame.mixer.Sound('sfx/Stand.wav'))
        self.add_sfx('run', pygame.mixer.Sound('sfx/Run.wav'))
        self.add_sfx('jump', pygame.mixer.Sound('sfx/Jump.wav'))
        self.add_sfx('kill', pygame.mixer.Sound('sfx/Kill.wav'))
        self.add_sfx('fall', pygame.mixer.Sound('sfx/Fall.wav'))
        self.add_sfx('lose', pygame.mixer.Sound('sfx/Lose.wav'))
        self.add_sfx('win', pygame.mixer.Sound('sfx/Win.wav'))
        self.add_sfx('longstun', pygame.mixer.Sound('sfx/LongStun.wav'))
        self.add_sfx('crash', pygame.mixer.Sound('sfx/Crash.wav'))

    def add_surface(self, name, surface):
        self.__surfaces[name] = surface

    def get_surface(self, name):
        return self.__surfaces[name]

    def del_surface(self, name):
        self.__surfaces.pop(name)

    def add_sfx(self, name, sfx):
        self.__sfx[name] = sfx

    def get_sfx(self, name):
        return self.__sfx[name]

    def del_sfx(self, name):
        self.__sfx.pop(name)

    def set_bg_color(self, color):
        self.__bg_color = color
        for the_gap in self.instance().gap_list:
            the_gap.switch_surface(color)

    def set_border_color(self, color):
        self.__border_color = color

    def create_floors(self):
        for i in range(8):
            the_floor = floor.Floor(i)
            self.floor_list.append(the_floor)
            self.sprite_group[GROUP_BCKGRND].add(the_floor)

    def increment_lives(self):
        self.lives += 1

    def decrement_lives(self):
        self.lives -= 1

    def draw_lives(self):
        life_frame = self.get_surface("life")
        for num in range(self.lives):
            self.screen.blit(life_frame, (zxx2x(num * ZX_LIFE_WIDTH), zxy2y(ZX_SCREEN_HEIGHT - ZX_LIFE_HEIGHT - 8)))

    def draw_score(self):
        txt = f"HI{self.highscore:05d} SC{self.score:05d}"
        font_surface = self.font.render(txt, False, SCORE_COLOR)
        w = font_surface.get_width()
        h = font_surface.get_height()
        self.screen.blit(font_surface, (zxx2x(ZX_SCREEN_WIDTH) - w, zxy2y(ZX_SCREEN_HEIGHT - 8) - h))

    def draw_background(self):
        self.screen.fill(Game.instance().__bg_color,
                         (SCALED_SCREEN_OFFSET_X, SCALED_SCREEN_OFFSET_Y,
                          zxw2w(ZX_SCREEN_WIDTH), zxh2h(ZX_SCREEN_HEIGHT)))

    def draw_borders(self):
        # top
        pygame.gfxdraw.box(self.screen,
                           (0, 0, DISPLAY_WIDTH, ZX_TOP_BORDER_HEIGHT * SCALE_FACTOR_Y),
                           self.__border_color)
        # bottom
        pygame.gfxdraw.box(self.screen,
                           (0, SCALED_BOTTOM_BORDER_Y, DISPLAY_WIDTH, ZX_BOTTOM_BORDER_HEIGHT * SCALE_FACTOR_Y),
                           self.__border_color)
        # left
        pygame.gfxdraw.box(self.screen,
                           (0, SCALED_SCREEN_OFFSET_Y, zxw2w(ZX_LEFT_BORDER_WIDTH), zxh2h(ZX_SCREEN_HEIGHT)),
                           self.__border_color)
        # right
        pygame.gfxdraw.box(self.screen,
                           (SCALED_RIGHT_BORDER_X, SCALED_SCREEN_OFFSET_Y, zxw2w(ZX_RIGHT_BORDER_WIDTH),
                            zxh2h(ZX_SCREEN_HEIGHT)),
                           self.__border_color)

    def update(self):
        if self.__new_state is not None:
            self.__state = self.__new_state
            self.__new_state = None
            self.__state.enter(self)

        if self.__state is not None:
            self.__state.handle_input(self)
            self.__state.update(self)

        if self.__new_state is not None:
            self.__state.exit(self)

    def change_state(self, new_state):
        if isinstance(new_state, type(self.__state)):
            return
        self.__new_state = new_state

    # ===================================================================================================
    #
    # main loop
    #
    # ===================================================================================================
    def run(self):
        self.change_state(LoaderState())

        run = True
        while run:
            self.clock.tick(FPS)

            # draw background
            self.draw_background()

            self.update()

            if self.is_border_draw_enabled():
               self.draw_borders()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    run = False

            pygame.display.flip()

    @staticmethod
    def instance():
        if Game.instance_ is None:
            Game.instance_ = Game()
        return Game.instance_

    @staticmethod
    def destroy():
        Game.instance_ = None


class GameState:
    def handle_input(self, game):
        pass

    def update(self, game):
        pass

    def enter(self, game):
        pass

    def exit(self, game):
        pass


# ===================================================================================================
# PlayingState
# ===================================================================================================
class PlayingState(GameState):
    def __init__(self):
        super().__init__()

    def enter(self, game):
        # create jack
        p = player.Player()

        # jack starting position
        p.set_position(zxx2x(ZX_SCREEN_WIDTH / 2) - (SCALED_PLAYER_WIDTH / 2),
                       zxy2y(ZX_SCREEN_HEIGHT - ZX_PLAYER_HEIGHT))
        game.sprite_group[GROUP_PLAYER].add(p)

        # create floors
        game.create_floors()

        # spawns 2 gaps
        floor_idx = 1
        floor_y = game.floor_list[floor_idx].rect.y
        gap.spawn_gap(zxx2x(128), floor_y, SCALED_GAP_SPEED, floor_idx, game.sprite_group[GROUP_BCKGRND])
        gap.spawn_gap(zxx2x(128), floor_y, -SCALED_GAP_SPEED, floor_idx, game.sprite_group[GROUP_BCKGRND])

        # spawns hazards
        if game.hazards > 0:
            for i in range(game.hazards):
                if len(game.hazard_list) < MAX_HAZARDS:
                    hazard.Hazard.spawn_hazard(game.sprite_group[GROUP_HAZARDS])

        # set background and border color
        game.set_bg_color(BACKGROUND_COLOR)
        game.set_border_color(BACKGROUND_COLOR)

    def update(self, game):
        # update sprites
        dt = game.clock.get_time() / 1000
        game.sprite_group[GROUP_BCKGRND].update(dt)
        game.sprite_group[GROUP_HAZARDS].update(dt)
        game.sprite_group[GROUP_PLAYER].update(dt)

        # draw floors and gaps
        game.sprite_group[GROUP_BCKGRND].draw(game.screen)

        # draw lives
        game.draw_lives()

        # draw score
        game.draw_score()

        # draw hazards
        game.sprite_group[GROUP_HAZARDS].draw(game.screen)
        # draw jack
        game.sprite_group[GROUP_PLAYER].draw(game.screen)

        # draw debug rect
        # player.draw_debug_rect()

    def exit(self, game):
        game.sprite_group[GROUP_BCKGRND].empty()
        game.sprite_group[GROUP_PLAYER].empty()
        game.sprite_group[GROUP_HAZARDS].empty()
        game.floor_list.clear()
        game.gap_list.clear()
        game.hazard_list.clear()


# ===================================================================================================
# LevelUpState
# ===================================================================================================
class LevelUpState(GameState):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.start_time = 0
        self.current_time = 0
        self.next_hazard = Game.instance().hazards + 1

        self.level_title = [
            ['Jumping Jack is quick and bold', 'With skill his story will unfold'],
            ['THE BALLAD OF JUMPING JACK', 'A daring explorer named Jack...'],
            ['Once found a peculiar track...', ''],
            ['There were dangers galore...', ''],
            ['Even holes in the floor...', ''],
            ['So he kept falling flat on', 'his back...'],
            ['Quite soon he got used to', 'the place...'],
            ['He could jump to escape from', 'the chase...'],
            ['But without careful thought...', ''],
            ['His leaps came to nought...', ''],
            ['And he left with a much', 'wider face...'],
            ['Things seemed just as bad as', 'could be...'],
            ['Hostile faces were all Jack', 'could see...'],
            ['He tried to stay calm...', ''],
            ['And to come to no harm...', ''],
            ['But more often got squashed', 'like a flea...'],
            ['By now Jack was in a', 'great flap...'],
            ['He felt like a rat in a trap...', ''],
            ['If only he''d guessed...', ''],
            ['That soon he could rest...', ''],
            ['After jumping the very', 'last gap.      - WELL DONE']
        ]

        self.rhyme = ['', '']
        self.rhyme_part_idx = 0
        self.rhyme_idx = [0, 0]
        self.rhyme_end = False
        self.fast_text = False

        self.extra_life = False
        self.extra_life_colours = [COLOR_BRIGHT_WHITE, COLOR_BRIGHT_MAGENTA]
        self.color_flash = None

    def handle_input(self, game):
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.fast_text = True

    def enter(self, game):
        self.clock = pygame.time.Clock()
        game.set_bg_color(COLOR_BASIC_YELLOW)
        game.set_border_color(COLOR_BASIC_YELLOW)

        self.color_flash = color_flash.ColorFlash(self.extra_life_colours, 250, 6)
        self.extra_life = self.next_hazard == 6 or self.next_hazard == 11 or self.next_hazard == 16
        if self.extra_life:
            game.increment_lives()

    def update(self, game):
        self.current_time += self.clock.tick()

        time_to_go = 125
        if self.fast_text:
            time_to_go = 30

        if (self.current_time - self.start_time > time_to_go) and not self.rhyme_end:
            self.start_time = self.current_time

            self.rhyme = self.level_title[game.hazards]
            rhyme_item = self.rhyme[self.rhyme_part_idx]
            self.rhyme_idx[self.rhyme_part_idx] += 1
            if self.rhyme_idx[self.rhyme_part_idx] >= len(rhyme_item):
                self.rhyme_idx[self.rhyme_part_idx] = len(rhyme_item)
                self.rhyme_part_idx += 1
                if self.rhyme_part_idx > 1:
                    self.rhyme_end = True

        pygame.gfxdraw.box(game.screen, (zxbx2x(8), zxby2y(2), zxbw2w(16), zxbh2h(3)), COLOR_BASIC_GREEN)
        font_surface = game.font.render(f'JUMPING JACK', False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (zxbx2x(10), zxby2y(3)))

        if self.next_hazard <= 20:
            pygame.gfxdraw.box(game.screen, (zxbx2x(2), zxby2y(8), zxbw2w(28), zxbh2h(3)), COLOR_BRIGHT_WHITE)
            txt = f'NEXT LEVEL - {self.next_hazard:>2}  HAZARDS'
            x = len(txt)
            if game.hazards == 0:
                x -= 1
            font_surface = game.font.render(txt[:x], False, COLOR_BASIC_BLUE)
            game.screen.blit(font_surface, (zxbx2x(4), zxby2y(9)))

        txt = self.rhyme[0][:self.rhyme_idx[0]]
        font_surface = game.font.render(f'{txt}', False, COLOR_BASIC_BLUE)
        game.screen.blit(font_surface, (zxbx2x(0), zxby2y(16)))

        if self.rhyme_idx[1] > 0:
            txt = self.rhyme[1][:self.rhyme_idx[1]]
            font_surface = game.font.render(f'{txt}', False, COLOR_BASIC_BLUE)
            game.screen.blit(font_surface, (zxbx2x(0), zxby2y(18)))

        if self.rhyme_end and self.extra_life:
            if not self.color_flash.is_enabled():
                self.color_flash.start()

            self.color_flash.update()
            box_color = self.color_flash.get_current_color() if self.color_flash.is_enabled() else COLOR_BRIGHT_MAGENTA
            txt_color = COLOR_BRIGHT_WHITE if box_color == COLOR_BRIGHT_MAGENTA else COLOR_BRIGHT_MAGENTA
            pygame.gfxdraw.box(game.screen, (zxbx2x(9), zxby2y(21), zxbw2w(14), zxbh2h(3)), box_color)
            font_surface = game.font.render('EXTRA LIFE', False, txt_color)
            game.screen.blit(font_surface, (zxbx2x(11), zxby2y(22)))

        if not self.color_flash.is_enabled() and self.rhyme_end and (self.current_time - self.start_time > 2000):
            if game.hazards >= 20:
                game.change_state(MenuState())
            else:
                game.hazards += 1
                game.change_state(PlayingState())
            return

    def exit(self, game):
        self.extra_life = False
        self.color_flash = None


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.new_high = False
        self.new_high_colours = [COLOR_BRIGHT_WHITE, COLOR_BRIGHT_MAGENTA]
        self.color_flash = None

    def enter(self, game):
        game.set_bg_color(COLOR_BASIC_YELLOW)
        game.set_border_color(COLOR_BASIC_YELLOW)

        if game.score > game.highscore:
            game.highscore = game.score
            self.new_high = True
            self.color_flash = color_flash.ColorFlash(self.new_high_colours, 1000, 5, 1000)
            self.color_flash.start()

    def handle_input(self, game):
        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
            game.restart()
            game.change_state(PlayingState())

    def update(self, game):
        pygame.gfxdraw.box(game.screen, (zxbx2x(8), zxby2y(2), zxbw2w(16), zxbh2h(3)), COLOR_BASIC_GREEN)
        font_surface = game.font.render(f'JUMPING JACK', False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (zxbx2x(10), zxby2y(3)))

        pygame.gfxdraw.box(game.screen, (zxbx2x(5), zxby2y(8), zxbw2w(22), zxbh2h(5)), COLOR_BASIC_CYAN)

        txt = f'FINAL SCORE  {game.score:05}'
        font_surface = game.font.render(txt, False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (zxbx2x(7), zxby2y(9)))

        txt = f'WITH  {game.hazards:>2}  HAZARDS'
        font_surface = game.font.render(txt, False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (zxbx2x(8), zxby2y(11)))

        if self.new_high:
            self.color_flash.update()
            box_color = self.color_flash.get_current_color() if self.color_flash.is_enabled() else COLOR_BRIGHT_MAGENTA
            txt_color = COLOR_BRIGHT_WHITE if box_color == COLOR_BRIGHT_MAGENTA else COLOR_BRIGHT_MAGENTA

            pygame.gfxdraw.box(game.screen, (zxbx2x(10), zxby2y(15), zxbw2w(12), zxbh2h(3)), box_color)
            font_surface = game.font.render('NEW HIGH', False, txt_color)
            game.screen.blit(font_surface, (zxbx2x(12), zxby2y(16)))

        font_surface = game.font.render('Press ENTER to replay', False, COLOR_BASIC_BLUE)
        game.screen.blit(font_surface, (zxbx2x(5), zxby2y(21)))

    def exit(self, game):
        self.new_high = False
        self.color_flash = None


# ===================================================================================================
# GameOverState
# ===================================================================================================
class LoaderState(GameState):
    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.elaped_ms = 0
        self.color_list = [COLOR_BASIC_BLACK,
                           COLOR_BASIC_BLUE,
                           COLOR_BASIC_RED,
                           COLOR_BASIC_MAGENTA,
                           COLOR_BASIC_GREEN,
                           COLOR_BASIC_CYAN,
                           COLOR_BASIC_YELLOW,
                           COLOR_BASIC_WHITE
                           ]
        self.color_idx = 0
        self.m = color_flash.MulticolorBorderFlash(2)

    def enter(self, game):
        frame = pygame.image.load(f'img/loader.gif')
        frame = pygame.transform.scale(frame, (SCALED_SCREEN_WIDTH, SCALED_SCREEN_HEIGHT))
        game.add_surface('intro', frame)
        game.border_draw_enable(False)

    def update(self, game):
        self.clock.tick()
        self.elaped_ms += self.clock.get_time()
        # game.set_border_color(self.color_list[self.color_idx])
        self.color_idx += 1
        if self.color_idx >= len(self.color_list):
            self.color_idx = 0

        game.screen.blit(game.get_surface('intro'), (SCALED_SCREEN_OFFSET_X, SCALED_SCREEN_OFFSET_Y))
        if self.elaped_ms > 3000 or SKIP_LOADER:
            game.change_state(MenuState())

        self.m.update()

    def exit(self, game):
        game.del_surface('intro')
        game.border_draw_enable(True)
