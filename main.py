import sys
import pygame
import math
import random
from pygame.locals import *

# Frames per second

FPS = 1000

# Global Constant Variables

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
LINE_THICKNESS = 10
PADDLE_SIZE = 50
PADDLE_OFFSET = 20

# Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
blue = pygame.Color('dodgerblue')

# Player Class

class Player:

	def __init__(self):

		# Starting Pos
		self.x = WINDOW_WIDTH/2 - LINE_THICKNESS/2
		self.y = WINDOW_HEIGHT/2 - LINE_THICKNESS/2
		# Rectangle
		self.rect = pygame.Rect(self.x, self.y, LINE_THICKNESS, LINE_THICKNESS)
		self.hit_rect = pygame.Rect(self.x, self.y, LINE_THICKNESS, LINE_THICKNESS)
		self.aim_dot = pygame.Rect(self.x, self.y, 2, 2)
		self.face_dir = "e"
		self.weapon = "fists"
		self.can_slash = True
		self.can_jump = False
		self.on_ground = False
		self.is_falling = True # for moving down
		self.is_jumping = False # for moving up

	def move_right(self, multiplier):
		self.rect.x += (3 * multiplier)
		self.hit_rect.x += (3 * multiplier)
		self.face_dir = "e"
	def move_left(self, multiplier):
		self.rect.x -= (3 * multiplier)
		self.hit_rect.x -= (3 * multiplier)
		self.face_dir = "w"
	def move_up(self, multiplier):
		self.rect.y -= (3 * multiplier)
		self.hit_rect.y -= (3 * multiplier)
		self.face_dir = "n"
	def move_down(self, multiplier):
		self.rect.y += (3 * multiplier)
		self.hit_rect.y += (3 * multiplier)
		self.face_dir = "s"


	def jump(self):
		self.is_jumping = True
		self.max_height = self.rect.y - 100


	def aim_move(self, mouse_x, mouse_y):
		self.aim_dot.x = mouse_x
		self.aim_dot.y = mouse_y

	def draw(self):
		pygame.draw.rect(display_surf, WHITE, self.rect)
		# pygame.draw.rect(display_surf, WHITE, self.aim_dot)
		pygame.draw.rect(display_surf, WHITE, self.hit_rect)

	def shoot(self, mouse_x, mouse_y):
		# print("Shooting")
		# make a new bullet
		# bullets.append(Bullet(self.rect.x, self.rect.y, mouse_x, mouse_y))
		pass

	def slash(self):

		if self.face_dir == "e":
		
			self.hit_rect.x = self.rect.x + LINE_THICKNESS

		elif self.face_dir == "w":
		
			self.hit_rect.x = self.rect.x - LINE_THICKNESS

		elif self.face_dir == "n":

			self.hit_rect.y = self.rect.y - LINE_THICKNESS

		elif self.face_dir == "s":

			self.hit_rect.y = self.rect.y + LINE_THICKNESS

	def slash_revert(self):

		self.hit_rect.x = self.rect.x
		self.hit_rect.y = self.rect.y

class Enemy:

	def __init__(self):

		self.type = "blah" # eventually for random enemies

		self.x = WINDOW_WIDTH
		self.y = WINDOW_HEIGHT

		self.rect = pygame.Rect(self.x, self.y, LINE_THICKNESS, LINE_THICKNESS)

	def move(self, dest_x, dest_y):

		if self.rect.x < dest_x:
			self.rect.x += 1
		if self.rect.x > dest_x:
			self.rect.x -= 1

		if self.rect.y > dest_y:
			self.rect.y -= 1
		if self.rect.y < dest_y:
			self.rect.y += 1

	def draw(self):

		pygame.draw.rect(display_surf, blue, self.rect)


class Bullet:

	def __init__(self, x, y, dest_x, dest_y):
	
		# Rectangle
		self.rect = pygame.Rect(x + LINE_THICKNESS/2 - 2, y + LINE_THICKNESS/2 - 2, 2, 4)
		self.alive = True
		self.dest_x = dest_x
		self.dest_y = dest_y

		self.calc_v()

	def calc_v(self):

		print("self x: " +str(self.rect.x))
		print("self dest x: " + str(self.dest_x))
		print("self y: " + str(self.rect.y))
		print("self dest y: " + str(self.dest_y))

		if self.rect.x > self.dest_x:
			self.slope_x = self.dest_x - self.rect.x
			print("slope_x: " + str(self.slope_x))
		elif self.rect.x < self.dest_x:
			self.slope_x = self.dest_x - self.rect.x
			print("slope_x: " + str(self.slope_x))
		else:
			self.slope_x = 0

		if self.rect.y > self.dest_y:
			self.slope_y = self.dest_y - self.rect.y
		elif self.rect.y < self.dest_y:
			self.slope_y = self.dest_y - self.rect.y
		else:
			self.slope_y = 0

		dist = math.sqrt((self.slope_x)**2 + (self.slope_y)**2)

		if(round(self.slope_x/dist) < 0):

			self.vel_x = round(self.slope_x/dist * 100) + 50

		elif(round(self.slope_x/dist) > 0):

			self.vel_x = round(self.slope_x/dist * 100) - 50

		else:
			self.vel_x = 0

		if(round(self.slope_y/dist) < 0):

			self.vel_y = round(self.slope_y/dist * 100) + 50

		elif(round(self.slope_y/dist) > 0):

			self.vel_y = round(self.slope_y/dist * 100) - 50

		else:
			self.vel_y = 0

		print(self.vel_x)
		print(self.vel_y)

	def move(self): # bullets will move to x and y

		self.rect.x += self.vel_x
		self.rect.y += self.vel_y


	def check_collision(self):
		# if collided, alive == false
		pass


	def draw(self):
		pygame.draw.rect(display_surf, WHITE, self.rect)

class Platform:

	def __init__(self, x, y, w, h):

		self.width = w
		self.height = h

		self.rect = pygame.Rect(x, y, w, h)

	def draw(self):
		pygame.draw.rect(display_surf, blue, self.rect)


# draws the arena --------------------------------------------------

def draw_arena():

	display_surf.fill((0, 0, 0))
	# Draw outline of arena
	#pygame.draw.rect(display_surf, WHITE, ((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS*2)
	# Draw centre line
	# pygame.draw.line(display_surf, WHITE, ((WINDOW_WIDTH/2), 0), ((WINDOW_WIDTH/2), WINDOW_HEIGHT), (int(LINE_THICKNESS/4)))


def check_slash_collision(enemy_rect, slash_rect):
	if enemy_rect.right >= slash_rect.left and enemy_rect.right <= slash_rect.right and enemy_rect.bottom > slash_rect.top and enemy_rect.top < slash_rect.bottom:
		return True
	if enemy_rect.left <= slash_rect.right and enemy_rect.right >= slash_rect.left and enemy_rect.bottom > slash_rect.top and enemy_rect.top < slash_rect.bottom:
		return True
	else:
		return False


def check_plat_collision(player_rect, plat_rect):
	if player_rect.bottom >= plat_rect.top and player_rect.bottom <= plat_rect.bottom and player_rect.right >= plat_rect.left and player_rect.left <= plat_rect.right:
		return True


# Displays the current score on the screen

'''def display_score(score):
	result_surf = BASIC_FONT.render('Score = %s' %(score), True, WHITE)
	result_rect = result_surf.get_rect()
	result_rect.topleft = (WINDOW_WIDTH - 150, 25)
	display_surf.blit(result_surf, result_rect)'''


# Main Function


def main():

	pygame.init()
	global display_surf

	global BASIC_FONT, BASIC_FONT_SIZE

	BASIC_FONT_SIZE = 20
	BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

	fps_clock = pygame.time.Clock()
	display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption('Dumpy')

	player = Player()

	enemies = []
	platforms = []

	multiplier = 1

	move_up = False
	move_down = False
	move_left = False
	move_right = False

	e_spawn_counter = 0

	# Draws the starting position of the Arena

	for i in range(2):
		platforms.append(Platform(WINDOW_WIDTH/2 - LINE_THICKNESS/2 + 50 * i, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 50 - 50 * (i), 50, 10))

	# platform = Platform(WINDOW_WIDTH/2 - LINE_THICKNESS/2, WINDOW_HEIGHT/2 - LINE_THICKNESS/2 + 50, 50, 10)

	draw_arena()
	# draw_paddle(paddle1)
	# draw_paddle(paddle2)

	player.draw()
	# platform.draw()

	for i in platforms:
		i.draw()

	is_on = -1

	pygame.mouse.set_visible(0)  # make cursor invisible

	mouse_x = 0
	mouse_y = 0

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
		if move_left:
			player.move_left(multiplier)


		draw_arena()
		player.draw()
		# platform.draw()

		for i in enemies:
			i.move(player.rect.x, player.rect.y)
			i.draw()
			if check_slash_collision(i.rect, player.hit_rect):
				enemies.remove(i)

		for i in range(len(platforms)):

			platforms[i].draw()

			if(check_plat_collision(player.rect, platforms[i].rect)):
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
				if player.rect.right < platforms[is_on].rect.left or player.rect.left > platforms[is_on].rect.right:
					player.is_falling = True
					is_on = -1

		if(player.is_falling):
			player.rect.y += 5
			player.hit_rect.y += 5

		if(player.is_jumping == True):
			if(player.rect.y > player.max_height):
				player.rect.y -= 5
				player.hit_rect.y -= 5
			else:
				player.is_jumping = False
				player.is_falling = True

		if(player.is_jumping == False and player.is_falling == False):
			player.can_jump = True

		if(player.is_falling == True):
			player.can_jump = False
			player.is_jumping = False


		pygame.display.update()


		fps_clock.tick(FPS)


if __name__ == '__main__':
	main()








