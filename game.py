import pygame
import pygame.gfxdraw

import hazard
import gap
import player
import line
import color_flash
from globals import *


# Singleton class
class Game:
    instance_ = None

    def __init__(self):
        self.bg_color = BACKGROUND_COLOR
        self.clock = pygame.time.Clock()
        self.surfaces = {}
        self.screen = pygame.display.get_surface()

        self.line_list = []
        self.gap_list = []
        self.life_list = []
        self.hazard_list = []
        self.sprite_group = {GROUP_BCKGRND: pygame.sprite.Group(), GROUP_HUD: pygame.sprite.Group(),
                             GROUP_HAZARDS: pygame.sprite.Group(), GROUP_PLAYER: pygame.sprite.Group()}

        self.lives = LIVES
        self.score = 0
        self.highscore = 0
        self.hazard = 0
        self.set_initial_hazard_value()

        self.font = pygame.font.Font('fonts/zxspectr.ttf', int(8 * SCALE_FACTOR_X))
        self.state = None
        self.new_state = None

    def set_initial_hazard_value(self):
        # level start from 0 (with no hazards) and runs until 20
        self.hazard = 1

    def set_bg_color(self, color):
        self.bg_color = color
        for the_gap in self.instance().gap_list:
            the_gap.switch_surface(color)

    def create_floors(self):
        for i in range(8):
            the_line = line.Line(i)
            self.line_list.append(the_line)
            self.sprite_group[GROUP_BCKGRND].add(the_line)

    def create_lives(self):
        life_frame = self.surfaces["life"]
        for num in range(self.lives):
            life = pygame.sprite.Sprite()
            life.rect = pygame.rect.Rect(((L_SCREEN_EDGE + (num * 8)) * SCALE_FACTOR_X, 176 * SCALE_FACTOR_Y),
                                         (life_frame.get_width(), life_frame.get_height()))
            life.image = life_frame
            self.life_list.append(life)
            self.sprite_group[GROUP_HUD].add(life)

    def decrement_lives(self):
        self.lives -= 1
        last_live = self.life_list[-1]
        del self.life_list[-1]
        self.sprite_group[GROUP_HUD].remove(last_live)

    def level_up(self):
        self.change_state(LevelUpState())

    def update(self):
        if self.new_state is not None:
            self.state = self.new_state
            self.new_state = None
            self.state.enter(self)

        if self.state is not None:
            self.state.handle_input(self)
            self.state.update(self)

        if self.new_state is not None:
            self.state.exit(self)

    def change_state(self, new_state):
        if isinstance(new_state, type(self.state)):
            return
        self.new_state = new_state

    # ===================================================================================================
    #
    # main loop
    #
    # ===================================================================================================
    def run(self):
        self.change_state(MenuState())

        run = True
        while run:
            self.clock.tick(FPS)

            # draw background
            self.screen.fill(Game.instance().bg_color)

            self.update()

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
        life_frame = pygame.image.load(f'img/life.png')
        life_frame = pygame.transform.scale(life_frame, SCALED_LIFE_SIZE)
        game.surfaces["life"] = life_frame

        # create player
        p = player.Player()

        # starting position
        p.set_position((ORIGINAL_RESOLUTION[0] - ORIGINAL_PLAYER_SIZE[0]) / 2 * SCALE_FACTOR_X,
                       176 * SCALE_FACTOR_Y)
        game.sprite_group[GROUP_PLAYER].add(p)

        # create floors
        game.create_floors()

        # spawns 2 gaps
        line1_y = game.line_list[1].rect.y
        gap.spawn_gap(o2x(128), line1_y, SCALED_GAP_SPEED, game.sprite_group[GROUP_BCKGRND])
        gap.spawn_gap(o2x(128), line1_y, -SCALED_GAP_SPEED, game.sprite_group[GROUP_BCKGRND])

        # spawns hazards
        if game.hazard > 0:
            for i in range(game.hazard):
                if len(game.hazard_list) < MAX_HAZARDS:
                    hazard.spawn_hazard(game.sprite_group[GROUP_HAZARDS])

        # create lives
        game.create_lives()

        # set background color
        game.set_bg_color(BACKGROUND_COLOR)

    def update(self, game):
        # draw score
        font_surface = game.font.render(f"HI{Game.instance().highscore:05d} SC{Game.instance().score:05d}",
                                        False, SCORE_COLOR)
        w = font_surface.get_width()
        game.screen.blit(font_surface, (SCALED_R_SCREEN_EDGE - w, 176 * SCALE_FACTOR_Y))

        # update sprites
        dt = game.clock.get_time() / 1000
        game.sprite_group[GROUP_BCKGRND].update(dt)
        game.sprite_group[GROUP_HAZARDS].update(dt)
        game.sprite_group[GROUP_PLAYER].update(dt)

        # draw sprites
        game.sprite_group[GROUP_BCKGRND].draw(game.screen)
        game.sprite_group[GROUP_HUD].draw(game.screen)
        game.sprite_group[GROUP_HAZARDS].draw(game.screen)
        game.sprite_group[GROUP_PLAYER].draw(game.screen)

        # draw debug rect
        # player.draw_debug_rect()

    def exit(self, game):
        game.sprite_group[GROUP_BCKGRND].empty()
        game.sprite_group[GROUP_HUD].empty()
        game.sprite_group[GROUP_PLAYER].empty()
        game.sprite_group[GROUP_HAZARDS].empty()
        game.line_list.clear()
        game.gap_list.clear()
        game.life_list.clear()
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
        self.next_hazard = Game.instance().hazard + 1

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

    def handle_input(self, game):
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.fast_text = True

    def enter(self, game):
        self.clock = pygame.time.Clock()
        game.set_bg_color(COLOR_BASIC_YELLOW)

    def update(self, game):
        self.current_time += self.clock.tick()

        time_to_go = 125
        if self.fast_text:
            time_to_go = 30

        if (self.current_time - self.start_time > time_to_go) and not self.rhyme_end:
            self.start_time = self.current_time

            self.rhyme = self.level_title[game.hazard]
            rhyme_item = self.rhyme[self.rhyme_part_idx]
            self.rhyme_idx[self.rhyme_part_idx] += 1
            if self.rhyme_idx[self.rhyme_part_idx] >= len(rhyme_item):
                self.rhyme_idx[self.rhyme_part_idx] = len(rhyme_item)
                self.rhyme_part_idx += 1
                if self.rhyme_part_idx > 1:
                    self.rhyme_end = True

        # original size of ZX Spectrum screen: (256, 192)
        # 8x8 blocks: (32, 24)
        pygame.gfxdraw.box(game.screen, (b2x(8), b2y(2), b2x(16), b2y(3)), COLOR_BASIC_GREEN)
        font_surface = game.font.render(f'JUMPING JACK', False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (b2x(10), b2y(3)))

        if self.next_hazard <= 20:
            pygame.gfxdraw.box(game.screen, (b2x(2), b2y(8), b2x(28), b2y(3)), COLOR_BRIGHT_WHITE)
            txt = f'NEXT LEVEL - {self.next_hazard:>2}  HAZARDS'
            x = len(txt)
            if game.hazard == 0:
                x -= 1
            font_surface = game.font.render(txt[:x], False, COLOR_BASIC_BLUE)
            game.screen.blit(font_surface, (b2x(4), b2y(9)))

        txt = self.rhyme[0][:self.rhyme_idx[0]]
        font_surface = game.font.render(f'{txt}', False, COLOR_BASIC_BLUE)
        game.screen.blit(font_surface, (b2x(0), b2y(16)))

        if self.rhyme_idx[1] > 0:
            txt = self.rhyme[1][:self.rhyme_idx[1]]
            font_surface = game.font.render(f'{txt}', False, COLOR_BASIC_BLUE)
            game.screen.blit(font_surface, (b2x(0), b2y(18)))

        if self.rhyme_end and (self.current_time - self.start_time > 2000):
            if game.hazard >= 20:
                game.change_state(MenuState())
            else:
                game.hazard += 1
                game.change_state(PlayingState())
            return

    def exit(self, game):
        pass


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.new_high = False
        self.new_high_colours = [COLOR_BRIGHT_WHITE, COLOR_BRIGHT_MAGENTA]
        self.color_flash = None

    def enter(self, game):
        game.set_bg_color(COLOR_BASIC_YELLOW)
        if game.score > game.highscore:
            game.highscore = game.score
            self.new_high = True
            self.color_flash = color_flash.ColorFlash(self.new_high_colours, 1000, 5, 1000)
            self.color_flash.start()

    def handle_input(self, game):
        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
            game.set_initial_hazard_value()
            game.change_state(PlayingState())

    def update(self, game):
        # original size of ZX Spectrum screen: (256, 192)
        # 8x8 blocks: (32, 24)
        pygame.gfxdraw.box(game.screen, (b2x(8), b2y(2), b2x(16), b2y(3)), COLOR_BASIC_GREEN)
        font_surface = game.font.render(f'JUMPING JACK', False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (b2x(10), b2y(3)))

        pygame.gfxdraw.box(game.screen, (b2x(5), b2y(8), b2x(22), b2y(5)), COLOR_BASIC_CYAN)

        txt = f'FINAL SCORE  {game.score:05}'
        font_surface = game.font.render(txt, False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (b2x(7), b2y(9)))

        txt = f'WITH  {game.hazard:>2}  HAZARDS'
        font_surface = game.font.render(txt, False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (b2x(8), b2y(11)))

        if self.new_high:
            self.color_flash.update()
            box_color = self.color_flash.get_current_color() if self.color_flash.is_enabled() else COLOR_BRIGHT_MAGENTA
            txt_color = COLOR_BRIGHT_WHITE if box_color == COLOR_BRIGHT_MAGENTA else COLOR_BRIGHT_MAGENTA

            pygame.gfxdraw.box(game.screen, (b2x(10), b2y(15), b2x(12), b2y(3)), box_color)
            font_surface = game.font.render('NEW HIGH', False, txt_color)
            game.screen.blit(font_surface, (b2x(12), b2y(16)))

        font_surface = game.font.render('Press ENTER to replay', False, COLOR_BASIC_BLUE)
        game.screen.blit(font_surface, (b2x(5), b2y(21)))

    def exit(self, game):
        self.new_high = False
        self.color_flash = None


# ===================================================================================================
# GameOverState
# ===================================================================================================
class GameOverState(GameState):
    pass
