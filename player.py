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
import game
import gap
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
        # idx of floor just above head
        self.floor_idx = 7

        # hidle animation
        hidle_anim = game_objects.Animation2D(True)
        hidle_anim.loop = True
        hidle_anim.speed = 1
        hidle_anim.add_frame(game_objects.AnimFrame2D(game.Game.instance().get_surface('idle1'), 0.75))
        hidle_anim.add_frame(game_objects.AnimFrame2D(game.Game.instance().get_surface('idle2'), 0.75))
        hidle_anim.add_frame(game_objects.AnimFrame2D(game.Game.instance().get_surface('idle1'), 0.75))
        hidle_anim.add_frame(game_objects.AnimFrame2D(game.Game.instance().get_surface('idle3'), 0.75))

        # walk animation
        walk_anim_right = game_objects.Animation2D(True)
        walk_anim_left = game_objects.Animation2D(True)
        for num in range(1, 5):
            walk_anim_right.add_frame(game_objects.AnimFrame2D(game.Game.instance().get_surface(f'walk_right{num}'), 0.05))
            walk_anim_left.add_frame(game_objects.AnimFrame2D(game.Game.instance().get_surface(f'walk_left{num}'), 0.05))
        walk_anim_right.loop = True
        walk_anim_right.speed = 1
        walk_anim_left.loop = True
        walk_anim_left.speed = 1

        # jump animation
        jump_anim = game_objects.Animation2D(True)
        for num in range(1, 4):
            frame = game.Game.instance().get_surface(f'jump{num}')
            jump_anim.add_frame(game_objects.AnimFrame2D(frame, 0.05))

        # electrified animation
        electrified_anim = game_objects.Animation2D(True)
        for num in range(1, 3):
            frame = game.Game.instance().get_surface(f'stunned{num}')
            electrified_anim.add_frame(game_objects.AnimFrame2D(frame, 0.50))

        # stunned animation
        stunned_anim = game_objects.Animation2D(True)
        for num in range(3, 7):
            frame = game.Game.instance().get_surface(f'stunned{num}')
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

    def has_gap_up(self):
        tollerance = 3 * SCALE_FACTOR_X

        for the_gap in game.Game.instance().gap_list:
            rect = the_gap.rect
            if abs(self.rect.y - rect.bottom) <= 7 * SCALE_FACTOR_Y:
                if self.rect.x >= (rect.x - tollerance) and self.rect.right <= (rect.right + tollerance):
                    return True
        return False

    def has_gap_down(self):
        for the_gap in game.Game.instance().gap_list:
            if abs(self.rect.bottom - the_gap.rect.y) <= SCALED_FLOOR_THICKNESS:
                if self.rect.x > the_gap.rect.x and self.rect.right < the_gap.rect.right:
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
        game.Game.instance().get_sfx("stand").play(-1)

    def handle_input(self, player):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            player.change_state(WalkingState())

        if key[pygame.K_UP]:
            player.change_state(JumpingState())

    def update(self, player, *args, **kwargs):
        if not CHEAT_HAZARD_IMMUNITY:
            if pygame.sprite.spritecollideany(player, game.Game.instance().sprite_group[GROUP_HAZARDS]) is not None:
                player.change_state(HazardHitState())

        if not CHEAT_FALL_IMMUNITY:
            if player.has_gap_down():
                player.change_state(FallingState())

    def exit(self, player):
        game.Game.instance().get_sfx("stand").stop()


class WalkingState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        game.Game.instance().get_sfx("run").play(-1)

    def handle_input(self, player):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-SCALED_PLAYER_SPEED, 0)
            if player.get_x() < SCALED_SCREEN_OFFSET_X:
                player.set_x(SCALED_RIGHT_BORDER_X - SCALED_PLAYER_WIDTH)
        elif key[pygame.K_RIGHT]:
            player.move(SCALED_PLAYER_SPEED, 0)
            if player.get_x() > SCALED_RIGHT_BORDER_X - SCALED_PLAYER_WIDTH:
                player.set_x(SCALED_SCREEN_OFFSET_X)
        else:
            player.change_state(HidleState())

    def update(self, player, dt):
        if player.direction == 1:
            player.set_animation(player.animations["walk_right"])
        else:
            player.set_animation(player.animations["walk_left"])

        if not CHEAT_HAZARD_IMMUNITY:
            if pygame.sprite.spritecollideany(player, game.Game.instance().sprite_group[GROUP_HAZARDS]) is not None:
                player.change_state(HazardHitState())

        if not CHEAT_FALL_IMMUNITY:
            if player.has_gap_down():
                player.change_state(FallingState())

    def exit(self, player):
        game.Game.instance().get_sfx("run").stop()


class JumpingState(PlayerState):
    def __init__(self):
        super().__init__()
        self.has_gap_up = True

    def enter(self, player):
        player.set_animation(player.animations["jump"])
        player.next_jump_y = game.Game.instance().floor_list[player.floor_idx].rect.y - SCALED_PLAYER_HEIGHT
        self.has_gap_up = player.has_gap_up()
        game.Game.instance().get_sfx("jump").play()

    def update(self, player, dt):
        player.move(0, -1.5 * SCALE_FACTOR_Y)

        if self.has_gap_up or CHEAT_JUMP_IMMUNITY:
            if player.floor_idx == 0 and player.y <= game.Game.instance().floor_list[0].rect.y:
                game.Game.instance().change_state(game.LevelUpState())
                game.Game.instance().get_sfx("jump").stop()
                game.Game.instance().get_sfx('win').play()
                pygame.time.delay(2000)
                return

            if player.y <= player.next_jump_y:
                player.y = player.next_jump_y
                player.floor_idx = player.floor_idx - 1
                player.next_jump_y = game.Game.instance().floor_list[player.floor_idx].rect.y - SCALED_PLAYER_HEIGHT
                grp = game.Game.instance().sprite_group[GROUP_BCKGRND]
                gap.spawn_random_gap(grp)
                game.Game.instance().score = game.Game.instance().score + 5
                player.change_state(HidleState())
        else:
            if player.y <= game.Game.instance().floor_list[player.floor_idx].rect.y:
                player.y = game.Game.instance().floor_list[player.floor_idx].rect.y
                player.change_state(ElectricfiedState())

    def exit(self, player):
        game.Game.instance().get_sfx("jump").stop()


class FallingState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.next_fallen_y = player.y + SCALED_FLOOR_DISTANCE
        game.Game.instance().get_sfx("fall").play()

    def update(self, player, dt):
        player.move(0, 5)
        if player.y >= player.next_fallen_y:
            player.y = player.next_fallen_y
            player.next_fallen_y = player.y + SCALED_FLOOR_DISTANCE
            player.floor_idx += 1
            player.change_state(StunnedState())

    def exit(self, player):
        game.Game.instance().get_sfx("fall").stop()


class HazardHitState(PlayerState):
    def __init__(self):
        super().__init__()
        self.flash = ScreenFlash((FLASH_COLOR_HAZARD_HIT, BACKGROUND_COLOR), 250, 1)

    def enter(self, player):
        self.flash.start()
        game.Game.instance().get_sfx("kill").play()

    def update(self, player, dt):
        self.flash.update()
        if not self.flash.is_enabled():
            player.change_state(StunnedState())

    def exit(self, player):
        self.flash.stop()
        game.Game.instance().get_sfx("kill").stop()


class ElectricfiedState(PlayerState):
    def __init__(self):
        super().__init__()
        self.flash = ScreenFlash((FLASH_COLOR_FLOOR_HIT, BACKGROUND_COLOR), 200, 3)

    def enter(self, player):
        player.set_animation(player.animations["electrified"])
        self.flash.start()

    def exit(self, player):
        self.flash.stop()

    def update(self, player, dt):
        self.flash.update()
        if player.get_animation().is_ended() and not self.flash.is_enabled():
            player.move(0, 8 * SCALE_FACTOR_Y)
            player.change_state(StunnedState())


class StunnedState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.set_animation(player.animations["stunned"])
        game.Game.instance().get_sfx('longstun').play()

    def exit(self, player):
        if not CHEAT_INFINITE_LIVES:
            if player.floor_idx == 7:
                game.Game().instance().decrement_lives()
                if game.Game.instance().lives < 1:
                    game.Game.instance().get_sfx('longstun').stop()
                    game.Game.instance().get_sfx('lose').play()
                    pygame.time.delay(2000)
                    game.Game.instance().change_state(game.MenuState())
        game.Game.instance().get_sfx('longstun').stop()

    def update(self, player, dt):
        if player.has_gap_down():
            player.change_state(HidleState())

        if player.get_animation().current_time > 1:
            player.change_state(HidleState())
