# http://torinak.com/qaop/games
# http://torinak.com/qaop#!jumpingjack

import random
import pygame
from pygame.font import Font

from game import Game
from globals import *

from player import *
from hole import Hole
from line import Line

from game_objects import Animation2D, AnimFrame2D, ZSprite

RESOLUTION = (800, 600)
DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF
# DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF|pygame.FULLSCREEN


# ------------------------------------inizio main --------------------------------------------
random.seed()
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(RESOLUTION, DISPLAY_MODE_FLAGS, vsync=1)
pygame.display.set_caption('Jumping Jack')

font = Font('fonts/Konsystem.ttf', 30)

# load images
# bg_img = pygame.image.load('img/background.png')

# definisce animazione hidle
hidle_anim = Animation2D(True)
pausa1 = pygame.image.load('img/idle1.png')
pausa2 = pygame.image.load('img/idle2.png')
pausa3 = pygame.image.load('img/idle3.png')
pausa1 = pygame.transform.scale(pausa1, SCALE_SIZE)
pausa2 = pygame.transform.scale(pausa2, SCALE_SIZE)
pausa3 = pygame.transform.scale(pausa3, SCALE_SIZE)
hidle_anim.loop = True
hidle_anim.speed = 1
hidle_anim.add_frame(AnimFrame2D(pausa1, 0.75))
hidle_anim.add_frame(AnimFrame2D(pausa2, 0.75))
hidle_anim.add_frame(AnimFrame2D(pausa1, 0.75))
hidle_anim.add_frame(AnimFrame2D(pausa3, 0.75))

# definisce animazione camminata
walk_anim_right = Animation2D(True)
walk_anim_left = Animation2D(True)
for num in range(1, 5):
    frame = pygame.image.load(f'img/walk{num}.png')
    frame = pygame.transform.scale(frame, SCALE_SIZE)
    walk_anim_right.add_frame(AnimFrame2D(frame, 0.05))
    frame = pygame.transform.flip(frame, True, False)
    walk_anim_left.add_frame(AnimFrame2D(frame, 0.05))
walk_anim_right.loop = True
walk_anim_right.speed = 1
walk_anim_left.loop = True
walk_anim_left.speed = 1

# definisce animazione salto
jump_anim = Animation2D(True)
for num in range(1, 4):
    frame = pygame.image.load(f'img/jump{num}.png')
    frame = pygame.transform.scale(frame, SCALE_SIZE)
    jump_anim.add_frame(AnimFrame2D(frame, 0.05))

# definisce animazione elettrificato
electrified_anim = Animation2D(True)
for num in range(1, 3):
    frame = pygame.image.load(f'img/stunned{num}.png')
    frame = pygame.transform.scale(frame, SCALE_SIZE)
    electrified_anim.add_frame(AnimFrame2D(frame, 0.50))

# definisce animazione stordito
stunned_anim = Animation2D(True)
for num in range(3, 7):
    frame = pygame.image.load(f'img/stunned{num}.png')
    frame = pygame.transform.scale(frame, SCALE_SIZE)
    stunned_anim.add_frame(AnimFrame2D(frame, 0.05))
    stunned_anim.loop = True

# 511 bottom
player = Player()
player.add_animation("hidle", hidle_anim)
player.add_animation("walk_right", walk_anim_right)
player.add_animation("walk_left", walk_anim_left)
player.add_animation("jump", jump_anim)
player.add_animation("electrified", electrified_anim)
player.add_animation("stunned", stunned_anim)
player.set_animation(hidle_anim)
player.set_position(383, 550 - SCALED_PLAYER_HEIGHT + 1)  # posizione iniziale

# crea gruppo di sprite
Game.instance().sprite_group[GROUP_BCKGRND] = pygame.sprite.Group()
Game.instance().sprite_group[GROUP_ENEMIES] = pygame.sprite.Group()
Game.instance().sprite_group[GROUP_PLAYER] = pygame.sprite.Group()

# lines
for i in range(0, 8):
    print(f'linea {i}: {70 + i * SPAZIO_TRA_LINEE}')
    linea = Line(L_SCREEN_EDGE, 70 + i * SPAZIO_TRA_LINEE)
    Game.instance().line_list.append(linea)
    Game.instance().sprite_group[GROUP_BCKGRND].add(linea)

# spawns 2 holes
Game.instance().spawn_hole(400, 130, HOLES_SPEED, Game.instance().sprite_group[GROUP_BCKGRND])
Game.instance().spawn_hole(400, 130, -HOLES_SPEED, Game.instance().sprite_group[GROUP_BCKGRND])

Game.instance().sprite_group[GROUP_PLAYER].add(player)

game = Game.instance()
game.bg_color = BACKGROUND_COLOR

run = True
while run:
    clock.tick(FPS)

    # disegna sfondo
    screen.fill(game.bg_color)

    # draw score
    font_surface = font.render(f"SC{Game.instance().score:05d}", False, (162, 27, 159))
    screen.blit(font_surface, (600, 510))

    # update sprites
    dt = clock.get_time() / 1000
    Game.instance().sprite_group[GROUP_BCKGRND].update(dt)
    Game.instance().sprite_group[GROUP_ENEMIES].update(dt)
    Game.instance().sprite_group[GROUP_PLAYER].update(dt)

    # disegna i gruppo di sprite
    Game.instance().sprite_group[GROUP_BCKGRND].draw(screen)
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
