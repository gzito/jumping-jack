# online zx spectrum emulator
# http://torinak.com/qaop/games
# http://torinak.com/qaop#!jumpingjack

import random

from pygame.font import Font
from pygame.sprite import Sprite

from line import Line
from player import *

DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF
# DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF|pygame.FULLSCREEN


# ------------------------------------inizio main --------------------------------------------
random.seed()
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(RESOLUTION, DISPLAY_MODE_FLAGS, vsync=1)
pygame.display.set_caption('Jumping Jack')


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

lifeFrame = pygame.image.load(f'img/life.png')
lifeFrame = pygame.transform.scale(lifeFrame, SCALED_LIFE_SIZE)

# create floors
Game.instance().create_floors()

# spawns 2 holes and place them inside GROUP_BCKGRND
line1_y = Game.instance().line_list[1].rect.y
Game.instance().spawn_hole(128 * SCALE_FACTOR_X, line1_y, SCALED_HOLE_SPEED,
                           Game.instance().sprite_group[GROUP_BCKGRND])
Game.instance().spawn_hole(128 * SCALE_FACTOR_X, line1_y, -SCALED_HOLE_SPEED,
                           Game.instance().sprite_group[GROUP_BCKGRND])

# create lives
for num in range(Game.instance().lives):
    life = Sprite()
    life.rect = Rect(((L_SCREEN_EDGE + (num * 8)) * SCALE_FACTOR_X, 176 * SCALE_FACTOR_Y),
                     (lifeFrame.get_width(), lifeFrame.get_height()))
    life.image = lifeFrame
    Game.instance().life_list.append(life)
    Game.instance().sprite_group[GROUP_HUD].add(life)

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
player.set_position((ORIGINAL_RESOLUTION[0] - ORIGINAL_PLAYER_SIZE[0]) / 2 * SCALE_FACTOR_X, 176 * SCALE_FACTOR_Y)
Game.instance().sprite_group[GROUP_PLAYER].add(player)


Game.instance().bg_color = BACKGROUND_COLOR


# ===================================================================================================
#
# main loop
#
# ===================================================================================================
run = True
while run:
    clock.tick(FPS)

    # draw background
    screen.fill(Game.instance().bg_color)

    # draw score
    font_surface = Game.instance().font.render(f"SC{Game.instance().score:05d}", False, SCORE_COLOR)
    font_surface = pygame.transform.scale(font_surface, (
        font_surface.get_width() * SCALE_FACTOR_X, font_surface.get_height() * SCALE_FACTOR_Y))
    w = font_surface.get_width()
    screen.blit(font_surface, (SCALED_R_SCREEN_EDGE-w, 176 * SCALE_FACTOR_Y))

    # update sprites
    dt = clock.get_time() / 1000
    Game.instance().sprite_group[GROUP_BCKGRND].update(dt)
    Game.instance().sprite_group[GROUP_ENEMIES].update(dt)
    Game.instance().sprite_group[GROUP_PLAYER].update(dt)

    # draw sprites
    Game.instance().sprite_group[GROUP_BCKGRND].draw(screen)
    Game.instance().sprite_group[GROUP_HUD].draw(screen)
    Game.instance().sprite_group[GROUP_ENEMIES].draw(screen)
    Game.instance().sprite_group[GROUP_PLAYER].draw(screen)

    # draw debug rect
    # player.draw_debug_rect()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            run = False

    pygame.display.flip()

Game.destroy()
pygame.font.quit()
pygame.quit()
