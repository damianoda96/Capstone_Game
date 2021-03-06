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
from Boss import *
from Textbox import *
from lang import *
#import pygame_textinput
import GIFImage

# Frames per second

FPS = 1000

# Global Constant Variables

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
LINE_THICKNESS = 10

# Colors

BLACK = (0, 0, 0)
black = (0, 0, 0)
WHITE = (255, 255, 255)
blue = pygame.Color('dodgerblue')
red = pygame.Color('firebrick1')
green = pygame.Color('chartreuse1')
grey = pygame.Color('gray20')

# Arena Sides:

left_side_rect = pygame.Rect(0,0, 10, WINDOW_HEIGHT)
right_side_rect = pygame.Rect(WINDOW_WIDTH - 10,0, 10, WINDOW_HEIGHT)

# commands

commands = []

# draws the arena --------------------------------------------------

def draw_title_screen():
	display_surf.fill((0, 0, 0))
	#pentagram = pygame.image.load('pentagram.jpg').convert()
	#pentagram = pygame.transform.scale(pentagram, (100, 100))
	#pentagram_rect = pentagram.get_rect()
	title_font = pygame.font.Font('freesansbold.ttf', 30)
	title_text = title_font.render('Platformer Demo', True, red)
	title_rect = title_text.get_rect()
	#pentagram_rect.topleft = (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 100)
	title_rect.topleft = (0, 0)
	display_surf.blit(title_text, title_rect)
	#display_surf.blit(pentagram, pentagram_rect)

def draw_problem_screen(current_level):
	if current_level == 1:
		problem_surf_0 = BASIC_FONT_1.render("Your Task: -Declare 2 integers", True, green)
		problem_surf_1 = BASIC_FONT_1.render("-Calculate their difference to equal 10", True, green)
		problem_surf_2 = BASIC_FONT_1.render("-Print to the Screen", True, green)
		problem_rect_0 = problem_surf_0.get_rect()
		problem_rect_1 = problem_surf_1.get_rect()
		problem_rect_2 = problem_surf_2.get_rect()
		problem_rect_0.topleft = (10, 15)
		problem_rect_1.topleft = (10, 30)
		problem_rect_2.topleft = (10, 45)
		display_surf.blit(problem_surf_0, problem_rect_0)
		display_surf.blit(problem_surf_1, problem_rect_1)
		display_surf.blit(problem_surf_2, problem_rect_2)

def draw_arena():
	display_surf.fill((0, 0, 0))

def draw_sides():
	pygame.draw.rect(display_surf, blue, left_side_rect)
	pygame.draw.rect(display_surf, blue, right_side_rect)

def display_command_prompt(current_text, y):
	text = BASIC_FONT.render(current_text,True,green)
	text_rect = text.get_rect()
	text_rect.topleft = (10, 15 * y)
	display_surf.blit(text, text_rect)

# Displays the death announcement

def display_death(current_text):
	result_surf = BASIC_FONT_1.render('YOU DIED', True, red)
	restart_surf = BASIC_FONT_1.render('Press Enter to Restart..', True, WHITE)
	result_rect = result_surf.get_rect()
	restart_rect = restart_surf.get_rect()
	result_rect.topleft = (WINDOW_WIDTH/2 - 50, 100)
	restart_rect.topleft = (WINDOW_WIDTH/2 - 50, 150)
	display_surf.blit(result_surf, result_rect)
	display_surf.blit(restart_surf, restart_rect)

def display_health(health, color, color2):
	health_font = pygame.font.Font('freesansbold.ttf', 10)

	health_bar_text = health_font.render('Health', True, color)
	health_bar_text_rect = health_bar_text.get_rect()
	health_bar_text_rect.topleft = (10,5)

	health_bar = pygame.Rect(11, 15, 15 * health, 5)
	health_bar_background = pygame.Rect(11, 15, 150, 5)

	pygame.draw.rect(display_surf, color2, health_bar_background)
	pygame.draw.rect(display_surf, color, health_bar)
	display_surf.blit(health_bar_text, health_bar_text_rect)


# Main Function

platforms = []

def main():

	# ____________ VARIABLE DECS _________________________

	pygame.init()
	global display_surf

	global BASIC_FONT, BASIC_FONT_SIZE, BASIC_FONT_1

	BASIC_FONT_SIZE = 15
	BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
	BASIC_FONT_1 = pygame.font.Font('freesansbold.ttf', 15)
	COMMAND_FONT = pygame.font.Font('freesansbold.ttf', 10)

	fps_clock = pygame.time.Clock()
	display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption('Platformer')

	player = Player.Player(WINDOW_WIDTH, WINDOW_HEIGHT, LINE_THICKNESS)

	finished = False

	current_text_lines = []

	# current_text = ""

	enemies = []

	multiplier = 1

	move_up = False
	move_down = False
	move_left = False
	move_right = False

	e_spawn_counter = 0

	is_dead = False

	last_is_on = 0

	platform_vel = 1

	start_ticks = pygame.time.get_ticks()

	level_type = "vertical"

	game_started = False

	command_displayed = False

	newline_counter = 1
	line_counter = 1

	current_text = "%s::~>> " % str(newline_counter)

	level_complete = False
	challenge_complete = False

	current_level = 1

	problem_displayed = False
	problem_solved = False

	# _______ IMAGE STUFF __________________

	blood_right = GIFImage.GIFImage("blood_anim_right.gif")
	blood_left = GIFImage.GIFImage("blood_anim_2.gif")

	# image example
	# pentagram = pygame.image.load('pentagram.png').convert()

	# ____________ SOUND STUFF ____________

	#music = pygame.mixer.Sound("generic_metal.wav")
	#channel = music.play()      # Sound plays at full volume by default
	#music.set_volume(0.9)


	# ________ LEVEL GENERATION ___________

	ground = 0

	# level 1

	for i in range(52):

		rand = random.randint(10, 300)
		rand_width = random.randint(30, 100)
		rand_type = random.randint(1,5)
		if rand_type == 2:
			t = "moving"
		else:
			t = "static"

		if i > 0 and i < 10:
			platforms.append(Platform.Platform(rand, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 100 - 50 * (i), rand_width, 10, t, 1))
		elif i >= 10 and i < 20:
			platforms.append(Platform.Platform(rand, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 100 - 50 * (i), rand_width, 10, t, 1))
		elif i >= 20 and i < 51:
			platforms.append(Platform.Platform(rand, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 100 - 50 * (i), rand_width, 10, t, 1))
		elif i == 0:
			platforms.append(Platform.Platform(10, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 100 - 50 * (i), 50, 10, "static", 1))
		elif i == 51:
			platforms.append(Platform.Platform(10, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + (100 - 50 * (i)) - 50, 2000, 10, "static", 1))
			ground = WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + (100 - 50 * (i)) - 50

	# level 2 ______

	for i in range(50):
		rand = random.randint(100, 300) 
		rand_width = random.randint(30, 100)
		platforms.append(Platform.Platform(400 + (i * 100), ground - (i * 100), rand_width, 10, "static", 0))


	# Draws the starting position of the Arena

	#draw_arena()

	#player.draw(display_surf, WHITE)

	#for i in platforms:
		#i.draw(display_surf, blue)

	draw_title_screen()

	is_on = -1

	pygame.mouse.set_visible(0)  # make cursor invisible

	mouse_x = 0
	mouse_y = 0

	gravity = 5

	boss_can_spawn = False
	boss_is_active = False

	boss = Boss(platforms[51].rect.x + 100, platforms[51].rect.y - 10, LINE_THICKNESS)

	text_flicker_counter = 0

	screen_flicker_counter = 0

	# ________________ START GAME LOOP ____________________________

	while True:  # main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEMOTION:
				mouse_x, mouse_y = event.pos
				player.aim_move(mouse_x, mouse_y)
          
			if event.type == pygame.KEYDOWN:
				if command_displayed:
					if len(current_text) <= 30:
						if event.key == pygame.K_a:
							current_text+= "a"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_b:
							current_text+="b"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_c:
							current_text+="c"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_d:
							current_text+="d"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_e:
							current_text+="e"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_f:
							current_text+="f"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_g:
							current_text+="g"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_h:
							current_text+="h"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_i:
							current_text+="i"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_j:
							current_text+="j"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_k:
							current_text+="k"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_l:
							current_text+="l"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_m:
							current_text+="m"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_n:
							current_text+="n"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_o:
							current_text+="o"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_p:
							current_text+="p"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_q:
							current_text+="q"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_r:
							current_text+="r"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_s:
							current_text+="s"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_t:
							current_text+="t"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_u:
							current_text+="u"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_v:
							current_text+="v"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_w:
							current_text+="w"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_x:
							current_text+="x"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_y:
							current_text+="y"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_z:
							current_text+="z"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_EQUALS:
							current_text+="="
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_SLASH:
							current_text+="/"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_PLUS:
							current_text+="+"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_KP_PLUS:
							current_text+="+"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_MINUS:
							current_text+="-"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_ASTERISK:
							current_text+="*"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_0:
							current_text+="0"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_1:
							current_text+="1"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_2:
							current_text+="2"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_3:
							current_text+="3"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_4:
							current_text+="4"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_5:
							current_text+="5"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_6:
							current_text+="6"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_7:
							current_text+="7"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_8:
							current_text+="8"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_9:
							current_text+="9"
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_SPACE:
							current_text+=" "
							text = BASIC_FONT.render(current_text, True, green)
						elif event.key == pygame.K_BACKSPACE:
							current_text = current_text[:-1]
							text = BASIC_FONT.render(current_text, True, green)
							

						elif event.key == pygame.K_RETURN:
							commands.append(Textbox(current_text, green, BASIC_FONT, newline_counter))
							if input_command(current_text):
								output = input_command(current_text)
								if level_complete:
									if output == 10:
										problem_solved = True
										command_displayed = False
										game_started = True
										current_level = 2
								newline_counter += 1
								commands.append(Textbox(str(output), green, BASIC_FONT, newline_counter))
							newline_counter += 1
							line_counter += 1

							current_text = "%s::~>> " % str(line_counter)
							# submit current_text to lang and move to next line
							pass

				if event.key==pygame.K_BACKQUOTE:
					if command_displayed == False:
						display_surf.fill((0, 0, 0))
						newline_counter = 1
						line_counter = 1
						game_started = False
						command_displayed = True
						display_command_prompt(current_text, newline_counter)
					else:
						if level_complete != True:
							game_started = True
							problem_solved = True
							command_displayed = False
						else:
							command_displayed = False

				if command_displayed:
					display_command_prompt(current_text, newline_counter)

				if event.key==pygame.K_a:
					if player.can_move_left:
						move_left = True
				if event.key==pygame.K_d:
					if player.can_move_right:
						move_right = True
				if event.key==pygame.K_LSHIFT:
					multiplier = 2
				if event.key==pygame.K_SPACE:
					if player.can_jump:
						# can_jump = False
						player.is_jumping = True
						player.can_jump = False
						if last_is_on < 51:
							player.jump(50)
						else:
							player.jump(100)
					if player.can_wall_jump:
						# can_wall_jump = False
						player.is_wall_jumping = True
						player.can_wall_jump = False
						if last_is_on < 51:
							player.wall_jump(30)
						else:
							player.wall_jump(60)
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
					if(game_started == False and command_displayed == False):
						game_started = True
					elif(game_started == False and command_displayed == True):
						for i in commands:
							i.draw(display_surf)
					if(is_dead):
						display_surf.fill((0, 0, 0))
						player.is_falling = False
						platforms.clear()
						main()

		if pygame.mouse.get_pressed()[0]:
			# player.shoot(mouse_x, mouse_y)
			pass

		# _______________ IF RETURN PRESSED, START GAME ________________

		if game_started:


			# _______ ENEMY SPAWNING _________________

			if platforms[is_on].type != "last" and current_level == 1:

				e_spawn_counter += 1

				if e_spawn_counter > 100:

					enemies.append(Enemy.Enemy())

					e_spawn_counter = 0

			# _______ PLAYER MOVEMENT _________________

			if move_right:
				if level_type == "vertical":
					if(player.rect.right < right_side_rect.left - 2):
						player.move_right(multiplier)
					else:
						player.rect.x = right_side_rect.x - 11
						player.hit_rect.x = right_side_rect.x - 11
						player.can_move_right = False
						if not player.is_wall_jumping:
							player.can_wall_jump = True
				if level_type == "horizontal":
					for i in platforms:
						i.move_left(4 * multiplier)
					left_side_rect.x -= (4 * multiplier)

					if(player.rect.x < 300):
						player.move_right(multiplier)


			if move_left:
				if level_type == "vertical":
					if(player.rect.left > left_side_rect.right + 2):
						player.move_left(multiplier)
					else:
						player.rect.x = left_side_rect.x + 11
						player.hit_rect.x = left_side_rect.x + 11
						player.can_move_left = False
						if not player.is_wall_jumping:
							player.can_wall_jump = True
				if  level_type == "horizontal":
					for i in platforms:
						i.move_right(4 * multiplier)
					left_side_rect.x += (4 * multiplier)
					if(player.rect.x > 100):
						player.move_left(multiplier)

			if player.rect.left > left_side_rect.right + 2:
				player.can_move_left = True
			if player.rect.right < right_side_rect.left - 2:
				player.can_move_right = True
			if player.rect.left > left_side_rect.right + 2 and player.rect.right < right_side_rect.left - 2:
				player.can_wall_jump = False

			# _______________ RANDOM DRAWING _________________________

			draw_arena()
			draw_sides()
			player.draw(display_surf, WHITE)

			# _______ BOSS STUFF _____________


			if boss_is_active:
				boss.move(right_side_rect, left_side_rect)
				boss.draw_health(display_surf, red, grey)
				if player.check_slash_collision(boss.rect):
					boss.health -= 1

			if (boss.health > 0):
				boss.draw(display_surf, red)
			else:
				boss_is_active = False
				boss.draw_health(display_surf, BLACK, BLACK)
				level_complete = True


			boss.rect.y = platforms[51].rect.y - (LINE_THICKNESS + 10)

			#________ IF LEVEL HAS COMPLETED __________

			if level_complete:
				game_started = False
				if problem_displayed == False and problem_solved == False:
					display_surf.fill((0, 0, 0))
					draw_problem_screen(current_level)
					problem_displayed = True
				if problem_solved:
					problem_displayed = False
					command_displayed = False
					current_level = 2
					level_complete = False
					game_started = True


			# draw you win stuff

			# ____________ ENEMY STUFF ________________

			for i in enemies:
				i.move(player.rect.x, player.rect.y)
				i.draw(display_surf)
				if player.check_slash_collision(i.rect):
					enemies.remove(i)
				if player.check_enemy_collision(i.rect):
					player.health -= 1
				if i.rect.top < platforms[51].rect.bottom:
					enemies.remove(i)

			# __________ PLATFORM STUFF ______________

			for i in range(len(platforms)):

				if platforms[i].rect.y > player.rect.y + 300:
					platforms[i].type = "inactive"

				if platforms[i].type is not "inactive":

					platforms[i].draw(display_surf, blue)
					platforms[i].rect.y += platforms[i].vel

					if platforms[i].type == "moving":
						platforms[i].side_move()

					if player.check_plat_collision(platforms[i].rect):
						is_on = i
						last_is_on = i
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
							player.can_jump = False

			# Increase platform speed

			if last_is_on >= 10 and last_is_on <= 20:
				for i in platforms:
					i.vel = 1
			elif last_is_on >= 21 and last_is_on < 50:
				for i in platforms:
					i.vel = 2
			elif last_is_on >= 49:
				if platforms[50].rect.y < platforms[51].rect.y + 250:
					platforms[51].vel = 1
				else:
					if current_level == 1:
						#if last_is_on == 51:
						for i in range(len(platforms)):
							if i > 51:
								platforms[i].set_plat_vel(0)
								platforms[i].type = "last"
						# platforms[51:].set_plat_vel(0)
						platforms[51].set_plat_vel(0)
						# platforms[51:].type = "last"
						platforms[51].type = "last"
						boss_is_active = True

			else:
				platform_vel = 0

			# Jumping stuff ---------------------------------

			if(player.is_falling):
				if(player.rect.y < player.max_height + 10):
					gravity = 3
				if(player.rect.y < player.max_height + 30):
					gravity = 5

				for i in platforms:
					if i.type != "last":
						i.rect.y -= gravity+1
				for i in enemies:
					i.rect.y -= gravity+1
				player.rect.y += gravity
				player.hit_rect.y += gravity

			if(player.is_wall_jumping):
				player.can_wall_jump = False
				if(player.rect.y > player.max_height):
					if(player.rect.y < player.max_height + 30):
						gravity = 3
					if(player.rect.y < player.max_height + 10):
						gravity = 1

					for i in platforms:
						if i.type != "last":
							i.rect.y += gravity+2
					for i in enemies:
						i.rect.y += gravity+2
					player.rect.y -= gravity
					player.hit_rect.y -= gravity
				else:
					player.is_wall_jumping = False
					player.is_falling = True


			if(player.is_jumping == True):
				player.can_jump = False
				if(player.rect.y > player.max_height):
					if(player.rect.y < player.max_height + 30):
						gravity = 3
					if(player.rect.y < player.max_height + 10):
						gravity = 1

					for i in platforms:
						if i.type != "last":
							i.rect.y += gravity+2
					for i in enemies:
						i.rect.y += gravity+2
					player.rect.y -= gravity
					player.hit_rect.y -= gravity
				else:
					player.is_jumping = False
					player.is_falling = True

			if(player.is_jumping == False and player.is_falling == False):
				player.can_jump = True
				player.rect.y += platforms[is_on].vel
				player.hit_rect.y += platforms[is_on].vel

			if(player.is_falling == True):
				player.can_jump = False
				player.is_jumping = False
				player.is_wall_jumping = False

			# --------------------------------------------

			# ________ LEVEL 2 ______________

			if game_started and problem_solved:
				#problem_solved = False
				current_level = 2
				level_type = "horizontal"
				right_side_rect.x += 2000
				for i in platforms:
					i.type = "static"



			if game_started:
				if problem_displayed:
					pass
				else:
					if player.health > 0:
						display_health(player.health, green, grey)
					else:
						display_surf.fill((0,0,0))
						display_death(current_text)
						is_dead = True
						game_started = False

			# check death

			if(platforms[last_is_on].rect.y < -200):
				display_surf.fill((0,0,0))
				display_death(current_text)
				is_dead = True
				game_started = False

			# -----------------------------------------


		pygame.display.update()


		fps_clock.tick(FPS)


if __name__ == '__main__':
	main()








