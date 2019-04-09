import sys
import pygame
import math
import random
from pygame.locals import *
import Player
import Enemy
import Platform
import Controller

LINE_THICKNESS = 10

# Player Class

class Player:

	def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, LINE_THICKNESS):

		# Starting Pos
		self.x = WINDOW_WIDTH/2 - LINE_THICKNESS/2 - 150
		self.y = WINDOW_HEIGHT/2 - LINE_THICKNESS/2
		self.health = 3;
		# Rectangle
		self.rect = pygame.Rect(self.x, self.y, LINE_THICKNESS, LINE_THICKNESS)
		self.hit_rect = pygame.Rect(self.x, self.y, LINE_THICKNESS, LINE_THICKNESS/2)
		self.aim_dot = pygame.Rect(self.x, self.y, 2, 2)
		self.face_dir = "e"
		self.weapon = "fists"
		self.can_slash = True
		self.can_jump = False
		self.on_ground = False
		self.is_falling = True # for moving down
		self.is_jumping = False # for moving up
		self.is_wall_jumping = False
		self.max_height = 0
		self.can_move_right = True
		self.can_move_left = True
		self.can_wall_jump = False
		self.can_double_jump = False

	def move_right(self, multiplier):
		self.rect.x += (4 * multiplier)
		self.hit_rect.x += (4 * multiplier)
		self.face_dir = "e"
	def move_left(self, multiplier):
		self.rect.x -= (4 * multiplier)
		self.hit_rect.x -= (4 * multiplier)
		self.face_dir = "w"
	def move_up(self, multiplier):
		self.rect.y -= (3 * multiplier)
		self.hit_rect.y -= (3 * multiplier)
		self.face_dir = "n"
	def move_down(self, multiplier):
		self.rect.y += (3 * multiplier)
		self.hit_rect.y += (3 * multiplier)
		self.face_dir = "s"


	def jump(self, max_h):
		self.is_jumping = True
		self.max_height = self.rect.y - max_h

	def wall_jump(self, max_h):
		self.is_wall_jumping = True
		self.max_height = self.rect.y - max_h


	def aim_move(self, mouse_x, mouse_y):
		self.aim_dot.x = mouse_x
		self.aim_dot.y = mouse_y

	def draw_health(self, display_surf, color):
		health_font = pygame.font.Font('freesansbold.ttf', 10)

		health_bar_text = health_font.render('Health', True, green)
		health_bar_text_rect = health_bar_text.get_rect()
		health_bar_text_rect.topleft = (10,5)

		health_bar = pygame.Rect(11, 15, 50 * self.health, 5)
		health_bar_background = pygame.Rect(11, 15, 30, 5)

		pygame.draw.rect(display_surf, grey, health_bar_background)
		pygame.draw.rect(display_surf, green, health_bar)
		display_surf.blit(health_bar_text, health_bar_text_rect)

	def draw(self, display_surf, color):
		pygame.draw.rect(display_surf, color, self.rect)
		# pygame.draw.rect(display_surf, WHITE, self.aim_dot)
		pygame.draw.rect(display_surf, color, self.hit_rect)

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

	def check_plat_collision(self, plat_rect):
		player_rect = self.rect
		if player_rect.bottom >= plat_rect.top and player_rect.bottom <= plat_rect.bottom and player_rect.right >= plat_rect.left and player_rect.left <= plat_rect.right and not self.is_jumping:
			return True

	def check_slash_collision(self, enemy_rect):

		slash_rect = self.hit_rect

		if enemy_rect.right >= slash_rect.left and enemy_rect.right <= slash_rect.right and enemy_rect.bottom > slash_rect.top and enemy_rect.top < slash_rect.bottom:
			return True
		if enemy_rect.left <= slash_rect.right and enemy_rect.right >= slash_rect.left and enemy_rect.bottom > slash_rect.top and enemy_rect.top < slash_rect.bottom:
			return True
		else:
			return False

