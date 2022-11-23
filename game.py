import pygame
import hole

from pygame.font import Font
from pygame.rect import Rect
from pygame.sprite import Sprite

from game_objects import Animation2D, AnimFrame2D
from globals import *
from line import Line
from player import Player


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
        self.sprite_group = {GROUP_BCKGRND: pygame.sprite.Group(), GROUP_HUD: pygame.sprite.Group(),
                             GROUP_ENEMIES: pygame.sprite.Group(), GROUP_PLAYER: pygame.sprite.Group()}

        self.lives = LIVES
        self.score = 0
        self.level = 1

        self.font = Font('fonts/zxspectr.ttf', 8)
        self.state = None
        self.new_state = None

    def set_bg_color(self, color):
        self.bg_color = color
        for hole in self.instance().hole_list:
            hole.switch_surface(color)

    def create_floors(self):
        for i in range(8):
            line = Line(i)
            self.line_list.append(line)
            self.sprite_group[GROUP_BCKGRND].add(line)

    def create_lives(self):
        life_frame = self.surfaces["life"]
        for num in range(self.lives):
            life = Sprite()
            life.rect = Rect(((L_SCREEN_EDGE + (num * 8)) * SCALE_FACTOR_X, 176 * SCALE_FACTOR_Y),
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
        # self.change_state(PlayingState())
        self.change_state(LevelUpState())

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


class PlayingState(GameState):
    def __init__(self):
        super().__init__()

    def enter(self, game):
        # hidle animation
        hidle_anim = Animation2D(True)
        pausa1 = pygame.image.load('img/player/idle1.png')
        pausa2 = pygame.image.load('img/player/idle2.png')
        pausa3 = pygame.image.load('img/player/idle3.png')
        pausa1 = pygame.transform.scale(pausa1, SCALED_PLAYER_SIZE)
        pausa2 = pygame.transform.scale(pausa2, SCALED_PLAYER_SIZE)
        pausa3 = pygame.transform.scale(pausa3, SCALED_PLAYER_SIZE)
        hidle_anim.loop = True
        hidle_anim.speed = 1
        hidle_anim.add_frame(AnimFrame2D(pausa1, 0.75))
        hidle_anim.add_frame(AnimFrame2D(pausa2, 0.75))
        hidle_anim.add_frame(AnimFrame2D(pausa1, 0.75))
        hidle_anim.add_frame(AnimFrame2D(pausa3, 0.75))

        # walk animation
        walk_anim_right = Animation2D(True)
        walk_anim_left = Animation2D(True)
        for num in range(1, 5):
            frame = pygame.image.load(f'img/player/walk{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            walk_anim_right.add_frame(AnimFrame2D(frame, 0.05))
            frame = pygame.transform.flip(frame, True, False)
            walk_anim_left.add_frame(AnimFrame2D(frame, 0.05))
        walk_anim_right.loop = True
        walk_anim_right.speed = 1
        walk_anim_left.loop = True
        walk_anim_left.speed = 1

        # jump animation
        jump_anim = Animation2D(True)
        for num in range(1, 4):
            frame = pygame.image.load(f'img/player/jump{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            jump_anim.add_frame(AnimFrame2D(frame, 0.05))

        # electrified animation
        electrified_anim = Animation2D(True)
        for num in range(1, 3):
            frame = pygame.image.load(f'img/player/stunned{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            electrified_anim.add_frame(AnimFrame2D(frame, 0.50))

        # stunned animation
        stunned_anim = Animation2D(True)
        for num in range(3, 7):
            frame = pygame.image.load(f'img/player/stunned{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            stunned_anim.add_frame(AnimFrame2D(frame, 0.05))
            stunned_anim.loop = True

        life_frame = pygame.image.load(f'img/life.png')
        life_frame = pygame.transform.scale(life_frame, SCALED_LIFE_SIZE)
        game.surfaces["life"] = life_frame

        # create player
        player = Player()
        player.add_animation("hidle", hidle_anim)
        player.add_animation("walk_right", walk_anim_right)
        player.add_animation("walk_left", walk_anim_left)
        player.add_animation("jump", jump_anim)
        player.add_animation("electrified", electrified_anim)
        player.add_animation("stunned", stunned_anim)
        player.set_animation(hidle_anim)
        # starting position
        player.set_position((ORIGINAL_RESOLUTION[0] - ORIGINAL_PLAYER_SIZE[0]) / 2 * SCALE_FACTOR_X,
                            176 * SCALE_FACTOR_Y)
        game.sprite_group[GROUP_PLAYER].add(player)

        # create floors
        game.create_floors()

        # spawns 2 holes and place them inside GROUP_BCKGRND
        line1_y = game.line_list[1].rect.y
        hole.spawn_hole(128 * SCALE_FACTOR_X, line1_y, SCALED_HOLE_SPEED, game.sprite_group[GROUP_BCKGRND])
        hole.spawn_hole(128 * SCALE_FACTOR_X, line1_y, -SCALED_HOLE_SPEED, game.sprite_group[GROUP_BCKGRND])

        # create lives
        game.create_lives()
        game.set_bg_color(BACKGROUND_COLOR)

    def update(self, game):
        # draw score
        font_surface = game.font.render(f"SC{Game.instance().score:05d}", False, SCORE_COLOR)
        font_surface = pygame.transform.scale(font_surface,
                                              (font_surface.get_width() * SCALE_FACTOR_X,
                                               font_surface.get_height() * SCALE_FACTOR_Y))
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


class LevelUpState(GameState):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.total_elapsed = 0

    def enter(self, game):
        self.clock = pygame.time.Clock()
        game.set_bg_color((255, 255, 0))

    def update(self, game):
        self.total_elapsed += self.clock.tick()

        if self.total_elapsed > 2000:
            game.change_state(PlayingState())
            return

        font_surface = game.font.render(f"NEXT LEVEL -  1   HAZARD", False, (0, 0, 255))
        font_surface = pygame.transform.scale(font_surface,
                                              (font_surface.get_width() * SCALE_FACTOR_X,
                                               font_surface.get_height() * SCALE_FACTOR_Y))
        w = font_surface.get_width()
        game.screen.blit(font_surface, (32 * SCALE_FACTOR_X, 92 * SCALE_FACTOR_Y))

    def exit(self, game):
        pass


class GameOverState(GameState):
    def __init__(self):
        super().__init__()
