import sys
import pygame
import math
import random
from pygame.locals import *
from Player import *
from Enemy import *
from Platform import *
from Controller import *
from Bullet import *

# Frames per second

FPS = 1000

# Global Constant Variables

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
LINE_THICKNESS = 10

# Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
blue = pygame.Color('dodgerblue')
red = pygame.Color('firebrick1')


# draws the arena --------------------------------------------------

def draw_arena():

	display_surf.fill((0, 0, 0))
	# Draw outline of arena
	#pygame.draw.rect(display_surf, WHITE, ((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS*2)
	# Draw centre line
	# pygame.draw.line(display_surf, WHITE, ((WINDOW_WIDTH/2), 0), ((WINDOW_WIDTH/2), WINDOW_HEIGHT), (int(LINE_THICKNESS/4)))


# Displays the death announcement

def display_death():
	result_surf = BASIC_FONT.render('YOU DIED', True, red)
	restart_surf = BASIC_FONT_1.render('Press Enter to Restart..', True, WHITE)
	result_rect = result_surf.get_rect()
	restart_rect = restart_surf.get_rect()
	result_rect.topleft = (WINDOW_WIDTH/2 - 50, 100)
	restart_rect.topleft = (WINDOW_WIDTH/2 - 50, 150)
	display_surf.blit(result_surf, result_rect)
	display_surf.blit(restart_surf, restart_rect)


# Main Function

platforms = []


def main():

	pygame.init()
	global display_surf

	global BASIC_FONT, BASIC_FONT_SIZE, BASIC_FONT_1

	BASIC_FONT_SIZE = 20
	BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
	BASIC_FONT_1 = pygame.font.Font('freesansbold.ttf', 15)

	fps_clock = pygame.time.Clock()
	display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption('Dumpy')

	player = Player.Player(WINDOW_WIDTH, WINDOW_HEIGHT, LINE_THICKNESS)

	enemies = []

	multiplier = 1

	move_up = False
	move_down = False
	move_left = False
	move_right = False

	e_spawn_counter = 0

	is_dead = False

	# Platform initialization

	for i in range(15):
		rand = random.randint(1, 300)
		rand_width = random.randint(30, 80)
		rand_type = random.randint(1,5)
		if rand_type == 2:
			t = "moving"
		else:
			t = "static"

		if i > 1:
			platforms.append(Platform(rand, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 100 - 50 * (i), rand_width, 10, t))
		else:
			platforms.append(Platform(0, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 100 - 50 * (i), 50, 10, "static"))

	# Draws the starting position of the Arena
	draw_arena()

	player.draw(display_surf, WHITE)

	for i in platforms:
		i.draw(display_surf, blue)

	is_on = -1

	pygame.mouse.set_visible(0)  # make cursor invisible

	mouse_x = 0
	mouse_y = 0

	gravity = 5

	while True:  # main game loop

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEMOTION:
				mouse_x, mouse_y = event.pos
				player.aim_move(mouse_x, mouse_y)
				# paddle1.y = mouse_y
          
			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_w:
					pass
					# move_up = True
				if event.key==pygame.K_a:
					move_left = True
				if event.key==pygame.K_s:
					pass
					# move_down = True
				if event.key==pygame.K_d:
					move_right = True
				if event.key==pygame.K_LSHIFT:
					multiplier = 2
				if event.key==pygame.K_SPACE:
					if player.can_jump:
						can_jump = False
						player.is_jumping = True
						player.jump()
				if event.key==pygame.K_f:
					if player.can_slash:
						player.slash()
					player.can_slash = False
					pass

			if event.type == pygame.KEYUP:
				if event.key==pygame.K_w:
					move_up = False
				if event.key==pygame.K_a:
					move_left = False
				if event.key==pygame.K_s:
					move_down = False
				if event.key==pygame.K_d:
					move_right = False
				if event.key==pygame.K_LSHIFT:
					while(float(multiplier) > 1):
						multiplier -= .05
				if event.key==pygame.K_SPACE:
					pass
				if event.key==pygame.K_f:
					player.slash_revert()
					player.can_slash = True
					pass
				if event.key==pygame.K_RETURN:
					if(is_dead):
						display_surf.fill((0, 0, 0))
						player.is_falling = False
						platforms.clear()
						main()

		if pygame.mouse.get_pressed()[0]:
			# player.shoot(mouse_x, mouse_y)
			pass

		'''e_spawn_counter += 1

		if e_spawn_counter > 100:

			enemies.append(Enemy())

			e_spawn_counter = 0'''

		if move_up:
			player.move_up(multiplier)
		if move_down:
			player.move_down(multiplier)
		if move_right:
			player.move_right(multiplier)
			for i in platforms:
				i.move_left(3 * multiplier)
		if move_left:
			player.move_left(multiplier)
			for i in platforms:
				i.move_right(3 * multiplier)

		draw_arena()
		player.draw(display_surf, WHITE)

		for i in enemies:
			i.move(player.rect.x, player.rect.y)
			i.draw(display_surf)
			if player.check_slash_collision(i.rect):
				enemies.remove(i)

		# ----- Platform collision handeling -----------------
		for i in range(len(platforms)):

			if platforms[i].rect.y > player.rect.y + 300:
				platforms[i].type = "inactive"

			if platforms[i].type is not "inactive":

				platforms[i].draw(display_surf, blue)
				platforms[i].rect.y += 1

				if platforms[i].type == "moving":
					platforms[i].side_move()

				if player.check_plat_collision(platforms[i].rect):
					is_on = i
					print(is_on)
					player.is_falling = False
					player.is_jumping = False
					player.rect.y = platforms[i].rect.y - platforms[i].height - 1
					player.hit_rect.y = platforms[i].rect.y - platforms[i].height - 1
					player.can_jump = True
					player.on_ground = True

		if(is_on > -1):
			if player.is_jumping == False:
				if platforms[is_on].type is not "inactive":
					if player.rect.right < platforms[is_on].rect.left or player.rect.left > platforms[is_on].rect.right:
						player.is_falling = True
						is_on = -1

		# Jumping stuff ---------------------------------

		if(player.is_falling):

			if(player.rect.y < player.max_height + 10):
				gravity = 3
			if(player.rect.y < player.max_height + 30):
				gravity = 5

			for i in platforms:
				i.rect.y -= gravity+1
			player.rect.y += gravity
			player.hit_rect.y += gravity

		if(player.is_jumping == True):
			if(player.rect.y > player.max_height):
				if(player.rect.y < player.max_height + 30):
					gravity = 3
				if(player.rect.y < player.max_height + 10):
					gravity = 1

				for i in platforms:
					i.rect.y += gravity+2
				player.rect.y -= gravity
				player.hit_rect.y -= gravity
			else:
				player.is_jumping = False
				player.is_falling = True

		if(player.is_jumping == False and player.is_falling == False):
			player.can_jump = True
			player.rect.y += 1
			player.hit_rect.y += 1

		if(player.is_falling == True):
			player.can_jump = False
			player.is_jumping = False

		# --------------------------------------------

		# check death

		if(platforms[0].rect.y < -50):
			display_death()
			is_dead = True

		# -----------------------------------------


		pygame.display.update()


		fps_clock.tick(FPS)


if __name__ == '__main__':
	main()








