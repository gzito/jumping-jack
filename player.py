from game import Game
from game_objects import *
from globals import *
from screen_flash import ScreenFlash


class Player(ZSprite):
    def __init__(self):
        super().__init__()
        self.state = HidleState()
        self.next_jump_y = 0
        self.next_fallen_y = 0
        # idx of line just above head
        self.line_idx = 7

    def update(self, *args, **kwargs):
        self.state.handle_input(self)
        self.state.update(self, *args)
        super().update(*args, **kwargs)
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
        # print(f'changing state from {self.state.__class__.__name__} to {new_state.__class__.__name__}')
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def has_hole_up(self):
        tollerance = 3 * SCALE_FACTOR_X

        for hole in Game.instance().hole_list:
            rect = hole.rect
            if abs(self.rect.y - rect.bottom) <= 7 * SCALE_FACTOR_Y:
                if self.rect.x >= (rect.x - tollerance) and self.rect.right <= (rect.right + tollerance):
                    return True
        return False

    def has_hole_down(self):
        for hole in Game.instance().hole_list:
            rect = hole.rect
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

        if self.has_hole_up:
            if player.line_idx == 0 and player.y <= Game.instance().line_list[0].rect.y:
                Game.instance().level_up()

            if player.y <= player.next_jump_y:
                player.y = player.next_jump_y
                player.next_jump_y = player.y - 25 * SCALE_FACTOR_Y
                player.line_idx = player.line_idx - 1
                player.change_state(HidleState())
                grp = Game.instance().sprite_group[GROUP_BCKGRND]
                Game.instance().spawn_random_hole(grp)
                Game.instance().score = Game.instance().score + 5
        else:
            if player.y <= Game.instance().line_list[player.line_idx].rect.y:
                player.y = Game.instance().line_list[player.line_idx].rect.y
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
            player.line_idx = player.line_idx + 1
            player.change_state(StunnedState())


class ElectricfiedState(PlayerState):
    def __init__(self):
        super().__init__()
        self.flash = ScreenFlash(BACKGROUND_COLOR, FLASH_COLOR, 200, 3)

    def enter(self, player):
        player.set_animation(player.animations["electrified"])
        self.flash.start()

    def exit(self, player):
        self.flash.stop()

    def update(self, player, dt):
        self.flash.update()
        if player.get_animation().is_ended():
            player.change_state(StunnedState())
            player.move(0, 8 * SCALE_FACTOR_Y)


class StunnedState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.set_animation(player.animations["stunned"])

    def exit(self, player):
        if player.line_idx == 7:
            Game().instance().decrement_lives()

    def update(self, player, dt):
        if player.has_hole_down():
            player.change_state(HidleState())

        if player.get_animation().current_time > 1:
            player.change_state(HidleState())


class DeadState(PlayerState):
    def __init__(self):
        super().__init__()
