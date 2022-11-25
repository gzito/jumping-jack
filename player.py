import pygame
import game
import hole
import game_objects
from globals import *
from screen_flash import ScreenFlash


class Player(game_objects.ZSprite):
    def __init__(self):
        super().__init__()
        self.state = HidleState()
        self.new_state = None
        self.next_jump_y = 0
        self.next_fallen_y = 0
        # idx of line just above head
        self.line_idx = 7

        # hidle animation
        hidle_anim = game_objects.Animation2D(True)
        pausa1 = pygame.image.load('img/player/idle1.png')
        pausa2 = pygame.image.load('img/player/idle2.png')
        pausa3 = pygame.image.load('img/player/idle3.png')
        pausa1 = pygame.transform.scale(pausa1, SCALED_PLAYER_SIZE)
        pausa2 = pygame.transform.scale(pausa2, SCALED_PLAYER_SIZE)
        pausa3 = pygame.transform.scale(pausa3, SCALED_PLAYER_SIZE)
        hidle_anim.loop = True
        hidle_anim.speed = 1
        hidle_anim.add_frame(game_objects.AnimFrame2D(pausa1, 0.75))
        hidle_anim.add_frame(game_objects.AnimFrame2D(pausa2, 0.75))
        hidle_anim.add_frame(game_objects.AnimFrame2D(pausa1, 0.75))
        hidle_anim.add_frame(game_objects.AnimFrame2D(pausa3, 0.75))

        # walk animation
        walk_anim_right = game_objects.Animation2D(True)
        walk_anim_left = game_objects.Animation2D(True)
        for num in range(1, 5):
            frame = pygame.image.load(f'img/player/walk{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            walk_anim_right.add_frame(game_objects.AnimFrame2D(frame, 0.05))
            frame = pygame.transform.flip(frame, True, False)
            walk_anim_left.add_frame(game_objects.AnimFrame2D(frame, 0.05))
        walk_anim_right.loop = True
        walk_anim_right.speed = 1
        walk_anim_left.loop = True
        walk_anim_left.speed = 1

        # jump animation
        jump_anim = game_objects.Animation2D(True)
        for num in range(1, 4):
            frame = pygame.image.load(f'img/player/jump{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            jump_anim.add_frame(game_objects.AnimFrame2D(frame, 0.05))

        # electrified animation
        electrified_anim = game_objects.Animation2D(True)
        for num in range(1, 3):
            frame = pygame.image.load(f'img/player/stunned{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            electrified_anim.add_frame(game_objects.AnimFrame2D(frame, 0.50))

        # stunned animation
        stunned_anim = game_objects.Animation2D(True)
        for num in range(3, 7):
            frame = pygame.image.load(f'img/player/stunned{num}.png')
            frame = pygame.transform.scale(frame, SCALED_PLAYER_SIZE)
            stunned_anim.add_frame(game_objects.AnimFrame2D(frame, 0.05))
            stunned_anim.loop = True

        self.add_animation("hidle", hidle_anim)
        self.add_animation("walk_right", walk_anim_right)
        self.add_animation("walk_left", walk_anim_left)
        self.add_animation("jump", jump_anim)
        self.add_animation("electrified", electrified_anim)
        self.add_animation("stunned", stunned_anim)

        self.set_animation(hidle_anim)

    def update(self, *args, **kwargs):
        if self.new_state is not None:
            self.state = self.new_state
            self.new_state = None
            self.state.enter(self)

        self.state.handle_input(self)
        self.state.update(self, *args)
        super().update(*args, **kwargs)
        if self.new_state is not None:
            self.state.exit(self)

        # print(f'{self.x},{self.y}')
        # print(f'self.line_idx: {self.line_idx}')

    # move the sprite of the given offset
    def move(self, dx=0.0, dy=0.0):
        super().move(dx, dy)
        if dx > 0:
            self.direction = 1
        else:
            self.direction = -1

    def change_state(self, new_state):
        if isinstance(new_state, type(self.state)):
            return
        self.new_state = new_state

    def has_hole_up(self):
        tollerance = 3 * SCALE_FACTOR_X

        for the_hole in game.Game.instance().hole_list:
            rect = the_hole.rect
            if abs(self.rect.y - rect.bottom) <= 7 * SCALE_FACTOR_Y:
                if self.rect.x >= (rect.x - tollerance) and self.rect.right <= (rect.right + tollerance):
                    return True
        return False

    def has_hole_down(self):
        for the_hole in game.Game.instance().hole_list:
            rect = the_hole.rect
            if abs(self.rect.bottom - rect.y) <= 1:
                if self.rect.x > rect.x and self.rect.right < rect.right:
                    return True
        return False


# -----------------------------------------------------------------
# Player states
#
class PlayerState:
    def __init__(self):
        super().__init__()

    def handle_input(self, player):
        pass

    def update(self, player, dt):
        pass

    def enter(self, player):
        pass

    def exit(self, player):
        pass


class HidleState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.set_animation(player.animations["hidle"])

    def handle_input(self, player):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            player.change_state(WalkingState())

        if key[pygame.K_UP]:
            player.change_state(JumpingState())

    def update(self, player, *args, **kwargs):
        if not CHEAT_HAZARD_IMMUNITY:
            if pygame.sprite.spritecollideany(player,game.Game.instance().sprite_group[GROUP_HAZARDS]) is not None:
                player.change_state(HazardHitState())

        if not CHEAT_HOLES_IMMUNITY:
            if player.has_hole_down():
                player.change_state(FallingState())


class WalkingState(PlayerState):
    def __init__(self):
        super().__init__()

    def handle_input(self, player):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-SCALED_PLAYER_SPEED, 0)
            if player.get_x() < SCALED_L_SCREEN_EDGE:
                player.set_x(SCALED_R_SCREEN_EDGE - SCALED_PLAYER_WIDTH)
        elif key[pygame.K_RIGHT]:
            player.move(SCALED_PLAYER_SPEED, 0)
            if player.get_x() > SCALED_R_SCREEN_EDGE - SCALED_PLAYER_WIDTH:
                player.set_x(SCALED_L_SCREEN_EDGE)
        else:
            player.change_state(HidleState())

    def update(self, player, dt):
        if player.direction == 1:
            player.set_animation(player.animations["walk_right"])
        else:
            player.set_animation(player.animations["walk_left"])

        if not CHEAT_HAZARD_IMMUNITY:
            if pygame.sprite.spritecollideany(player,game.Game.instance().sprite_group[GROUP_HAZARDS]) is not None:
                player.change_state(HazardHitState())

        if not CHEAT_HOLES_IMMUNITY:
            if player.has_hole_down():
                player.change_state(FallingState())


class JumpingState(PlayerState):
    def __init__(self):
        super().__init__()
        self.has_hole_up = True

    def enter(self, player):
        player.set_animation(player.animations["jump"])
        player.next_jump_y = player.y - 24 * SCALE_FACTOR_Y
        self.has_hole_up = player.has_hole_up()

    def update(self, player, dt):
        player.move(0, -1.5 * SCALE_FACTOR_Y)

        if self.has_hole_up or CHEAT_JUMP_IMMUNITY:
            if player.line_idx == 0 and player.y <= game.Game.instance().line_list[0].rect.y:
                game.Game.instance().level_up()
                pygame.time.delay(1000)
                return

            if player.y <= player.next_jump_y:
                player.y = player.next_jump_y
                player.next_jump_y = player.y - 25 * SCALE_FACTOR_Y
                player.line_idx = player.line_idx - 1
                grp = game.Game.instance().sprite_group[GROUP_BCKGRND]
                hole.spawn_random_hole(grp)
                game.Game.instance().score = game.Game.instance().score + 5
                player.change_state(HidleState())
        else:
            if player.y <= game.Game.instance().line_list[player.line_idx].rect.y:
                player.y = game.Game.instance().line_list[player.line_idx].rect.y
                player.change_state(ElectricfiedState())


class FallingState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.next_fallen_y = player.y + 24 * SCALE_FACTOR_Y

    def update(self, player, dt):
        player.move(0, 5)
        if player.y >= player.next_fallen_y:
            player.y = player.next_fallen_y
            player.next_fallen_y = player.y + 24 * SCALE_FACTOR_Y
            player.line_idx += 1
            player.change_state(StunnedState())


class HazardHitState(PlayerState):
    def __init__(self):
        super().__init__()
        self.flash = ScreenFlash(BACKGROUND_COLOR, FLASH_COLOR_HAZARD_HIT, 250, 2)

    def enter(self, player):
        self.flash.start()

    def exit(self, player):
        self.flash.stop()

    def update(self, player, dt):
        self.flash.update()
        if not self.flash.is_enabled():
            player.change_state(StunnedState())


class ElectricfiedState(PlayerState):
    def __init__(self):
        super().__init__()
        self.flash = ScreenFlash(BACKGROUND_COLOR, FLASH_COLOR_FLOOR_HIT, 200, 3)

    def enter(self, player):
        player.set_animation(player.animations["electrified"])
        self.flash.start()

    def exit(self, player):
        self.flash.stop()

    def update(self, player, dt):
        self.flash.update()
        if player.get_animation().is_ended():
            player.move(0, 8 * SCALE_FACTOR_Y)
            player.change_state(StunnedState())


class StunnedState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.set_animation(player.animations["stunned"])

    def exit(self, player):
        if not CHEAT_INFINITE_LIVES:
            if player.line_idx == 7:
                game.Game().instance().decrement_lives()

    def update(self, player, dt):
        if player.has_hole_down():
            player.change_state(HidleState())

        if player.get_animation().current_time > 1:
            player.change_state(HidleState())

