# http://torinak.com/qaop/games
# http://torinak.com/qaop#!jumpingjack

import random
import pygame

from globals import *

from player import *
from hole import Hole
from line import Line


from game_objects import Animation2D, AnimFrame2D, ZSprite

RESOLUTION = (800, 600)
DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF
# DISPLAY_MODE_FLAGS = pygame.DOUBLEBUF|pygame.FULLSCREEN

def spawn_hole(x,y,speed,grp):
	hole = Hole(x, y)
	hole.vel = speed
	grp.add(hole)
	hole_list.append(hole)
	return hole

# ------------------------------------inizio main --------------------------------------------

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(RESOLUTION,DISPLAY_MODE_FLAGS,vsync=1)
pygame.display.set_caption('Jumping Jack')

background_color = (181, 178, 184) ;

#load images
#bg_img = pygame.image.load('img/background.png')

# definisce animazione hidle
hidle_anim = Animation2D(True)
pausa1 = pygame.image.load('img/walk1.png')
pausa2 = pygame.image.load('img/pausa2.png')
pausa3 = pygame.image.load('img/pausa3.png')
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
for num in range(2, 6):
	frame = pygame.image.load(f'img/walk{num}.png')
	frame = pygame.transform.scale(frame,SCALE_SIZE)
	walk_anim_right.add_frame(AnimFrame2D(frame, 0.05))
	frame = pygame.transform.flip(frame,True,False)
	walk_anim_left.add_frame(AnimFrame2D(frame, 0.05))
walk_anim_right.loop = True
walk_anim_right.speed = 1
walk_anim_left.loop = True
walk_anim_left.speed = 1

# definisce animazione salto
jump_anim = Animation2D(True)
for num in range(1, 4):
	frame = pygame.image.load(f'img/jump{num}.png')
	frame = pygame.transform.scale(frame,SCALE_SIZE)
	jump_anim.add_frame(AnimFrame2D(frame, 0.05))

# definisce animazione elettrificato
electrified_anim = Animation2D(True)
for num in range(1, 3):
	frame = pygame.image.load(f'img/morto{num}.png')
	frame = pygame.transform.scale(frame,SCALE_SIZE)
	electrified_anim.add_frame(AnimFrame2D(frame, 0.50))

# definisce animazione stordito
stunned_anim = Animation2D(True)
for num in range(3, 7):
	frame = pygame.image.load(f'img/morto{num}.png')
	frame = pygame.transform.scale(frame,SCALE_SIZE)
	stunned_anim.add_frame(AnimFrame2D(frame, 0.05))
	stunned_anim.loop = True



#511 bottom
player = Player()
player.add_animation("hidle", hidle_anim)
player.add_animation("walk_right",walk_anim_right)
player.add_animation("walk_left",walk_anim_left)
player.add_animation("jump",jump_anim)
player.add_animation("electrified", electrified_anim)
player.add_animation("stunned", stunned_anim)
player.set_animation(hidle_anim)
player.set_position(383, 550-SCALED_PLAYER_HEIGHT+1)  # posizione iniziale

# crea gruppo di sprite
grp = pygame.sprite.Group()

#lines
for i in range(0,8):
	print(f'linea {i}: {70+i*SPAZIO_TRA_LINEE}' )
	linea = Line(0, 70 + i * SPAZIO_TRA_LINEE)
	line_list.append(linea)
	grp.add(linea)

# hole
spawn_hole(400,130, HOLES_SPEED,grp)
spawn_hole(400,130,-HOLES_SPEED,grp)

grp.add(player)


run = True
while run:

	clock.tick(FPS)

# key = pygame.key.get_pressed()

	# disegna sfondo
	#screen.blit(bg_img, (0, 0))
	screen.fill(background_color)

	# disegna il gruppo di sprite
	grp.draw(screen)

	# draw debug rect
	# player.draw_debug_rect()

	# update sprites
	grp.update(clock.get_time()/1000)

	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key==pygame.K_ESCAPE):
			run = False

	pygame.display.flip()

pygame.quit()
