from game_objects import *
from globals import *


class Player(ZSprite):
    def __init__(self):
        # chiama init della classe padre (ZSprite)
        super().__init__()
        self.state = HidleState()
        # self.next_jump_y = 490 - SCALED_PLAYER_HEIGHT + 2
        # self.next_fallen_y = 550 - SCALED_PLAYER_HEIGHT + 2
        self.next_jump_y = 0
        self.next_fallen_y = 0

        self.linea_sopra = 7

    def update(self, *args, **kwargs):
        self.state.handle_input(self)
        self.state.update(self, *args)
        super().update(*args, **kwargs)  # chiama update() della classe padre ZSprite
        # print(f'{self.rect.x},{self.rect.y}')

    def move(self, dx, dy):
        super().move(dx, dy)  # disegna lo sprite spostato
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
        tollerance = 10

        for hole in hole_list:
            rect = hole.rect
            if abs(self.rect.y - rect.bottom) <= 20:
                if self.rect.x >= (rect.x - tollerance) and self.rect.right <= (rect.right + tollerance):
                    # print('has_hole_up')
                    return True
        return False

    def has_hole_down(self):
        for hole in hole_list:
            rect = hole.rect
            if abs(self.rect.bottom - rect.y) <= 1:
                if self.rect.x > rect.x and self.rect.right < rect.right:
                    # print('has_hole_down=true')
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
            player.move(-5, 0)
            if player.get_x() < 0 - SCALED_PLAYER_WIDTH:
                player.set_x(800 + SCALED_PLAYER_WIDTH)
        elif key[pygame.K_RIGHT]:
            player.move(5, 0)
            if player.get_x() > 800:
                player.set_x(0)
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
        player.next_jump_y = player.y - 60
        self.has_hole_up = player.has_hole_up()

    def update(self, player, dt):
        player.move(0, -4)

        if self.has_hole_up:
            if player.y <= player.next_jump_y:
                player.y = player.next_jump_y
                player.next_jump_y = player.y - 60
                player.linea_sopra = player.linea_sopra - 1
                player.change_state(HidleState())
        else:
            if player.y <= line_list[player.linea_sopra].rect.y:
                player.y = line_list[player.linea_sopra].rect.y
                player.change_state(ElectricfiedState())


class FallingState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.next_fallen_y = player.y + 60

    def update(self, player, dt):
        player.move(0, 5)
        if player.y >= player.next_fallen_y:
            player.y = player.next_fallen_y
            player.next_fallen_y = player.y + 60
            player.linea_sopra = player.linea_sopra + 1
            player.change_state(StunnedState())


class ElectricfiedState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.set_animation(player.animations["electrified"])

    def update(self, player, dt):
        if player.get_animation().is_ended():
            player.change_state(StunnedState())
            player.move(0, 21)


class StunnedState(PlayerState):
    def __init__(self):
        super().__init__()

    def enter(self, player):
        player.set_animation(player.animations["stunned"])

    def update(self, player, dt):
        if player.get_animation().current_time > 3:
            player.change_state(HidleState())


class DeadState(PlayerState):
    def __init__(self):
        super().__init__()
