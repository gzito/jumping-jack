import pygame
import pygame.gfxdraw

import enemy
import hole
import player
import line
import game_objects
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
        self.hole_list = []
        self.life_list = []
        self.enemy_list = []
        self.sprite_group = {GROUP_BCKGRND: pygame.sprite.Group(), GROUP_HUD: pygame.sprite.Group(),
                             GROUP_ENEMIES: pygame.sprite.Group(), GROUP_PLAYER: pygame.sprite.Group()}

        self.lives = LIVES
        self.score = 0
        self.hazard = 10  # level start from 0 (with no hazards) and runs until 20

        self.font = pygame.font.Font('fonts/zxspectr.ttf', int(8 * SCALE_FACTOR_X))
        self.state = None
        self.new_state = None

    def set_bg_color(self, color):
        self.bg_color = color
        for the_hole in self.instance().hole_list:
            the_hole.switch_surface(color)

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

        # spawns 2 holes
        line1_y = game.line_list[1].rect.y
        hole.spawn_hole(o2x(128), line1_y, SCALED_HOLE_SPEED, game.sprite_group[GROUP_BCKGRND])
        hole.spawn_hole(o2x(128), line1_y, -SCALED_HOLE_SPEED, game.sprite_group[GROUP_BCKGRND])

        # spawns enemies
        if game.hazard > 0:
            for i in range(game.hazard):
                enemy.spawn_random_enemy(game.sprite_group[GROUP_ENEMIES])

        # create lives
        game.create_lives()

        # set background color
        game.set_bg_color(BACKGROUND_COLOR)

    def update(self, game):
        # draw score
        font_surface = game.font.render(f"SC{Game.instance().score:05d}", False, SCORE_COLOR)
        w = font_surface.get_width()
        game.screen.blit(font_surface, (SCALED_R_SCREEN_EDGE - w, 176 * SCALE_FACTOR_Y))

        # update sprites
        dt = game.clock.get_time() / 1000
        game.sprite_group[GROUP_BCKGRND].update(dt)
        game.sprite_group[GROUP_ENEMIES].update(dt)
        game.sprite_group[GROUP_PLAYER].update(dt)

        # draw sprites
        game.sprite_group[GROUP_BCKGRND].draw(game.screen)
        game.sprite_group[GROUP_HUD].draw(game.screen)
        game.sprite_group[GROUP_ENEMIES].draw(game.screen)
        game.sprite_group[GROUP_PLAYER].draw(game.screen)

        # draw debug rect
        # player.draw_debug_rect()

    def exit(self, game):
        game.sprite_group[GROUP_BCKGRND].empty()
        game.sprite_group[GROUP_HUD].empty()
        game.sprite_group[GROUP_PLAYER].empty()
        game.sprite_group[GROUP_ENEMIES].empty()
        game.line_list.clear()
        game.hole_list.clear()
        game.life_list.clear()


# ===================================================================================================
# LevelUpState
# ===================================================================================================
class LevelUpState(GameState):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.start_time = 0
        self.current_time = 0
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

    def enter(self, game):
        self.clock = pygame.time.Clock()
        game.hazard += 1
        game.set_bg_color(COLOR_BASIC_YELLOW)

    def update(self, game):
        self.current_time += self.clock.tick()
        if (self.current_time - self.start_time > 125) and not self.rhyme_end:
            self.start_time = self.current_time

            self.rhyme = self.level_title[game.hazard - 1]
            rhyme_item = self.rhyme[self.rhyme_part_idx]
            self.rhyme_idx[self.rhyme_part_idx] += 1
            if self.rhyme_idx[self.rhyme_part_idx] >= len(rhyme_item):
                self.rhyme_idx[self.rhyme_part_idx] = len(rhyme_item)
                self.rhyme_part_idx += 1
                if self.rhyme_part_idx > 1:
                    self.rhyme_end = True

        # original size of ZX Spectrum screen: (256, 192)
        # 8x8 blocks: (32, 24)
        pygame.gfxdraw.box(game.screen, (b2x(9), b2y(2), b2x(16), b2y(3)), COLOR_BASIC_GREEN)
        font_surface = game.font.render(f'JUMPING JACK', False, COLOR_BASIC_BLACK)
        game.screen.blit(font_surface, (b2x(11), b2y(3)))

        pygame.gfxdraw.box(game.screen, (b2x(2), b2y(8), b2x(28), b2y(3)), COLOR_BRIGHT_WHITE)
        txt = f'NEXT LEVEL - {game.hazard:>2}  HAZARDS'
        x = len(txt)
        if game.hazard == 1:
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
            game.change_state(PlayingState())
            return

    def exit(self, game):
        pass


class MenuState(GameState):
    def __init__(self):
        super().__init__()

    def enter(self, game):
        game.set_bg_color(COLOR_BASIC_YELLOW)

    def handle_input(self, game):
        key = pygame.key.get_pressed()

        if key[pygame.K_RETURN]:
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

        txt = 'Press ENTER to replay'
        font_surface = game.font.render(txt, False, COLOR_BASIC_BLUE)
        game.screen.blit(font_surface, (b2x(5), b2y(21)))


# ===================================================================================================
# GameOverState
# ===================================================================================================
class GameOverState(GameState):
    pass
