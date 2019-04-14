import sys
import pygame
import math
import random
from pygame.locals import *
import Player
import Enemy
import Platform
import Controller

class Boss:
	
	def __init__(self, x, y, LINE_THICKNESS):
		self.x = x
		self.y = y
		self.move_left = False
		self.move_right = True
		self.rect = pygame.Rect(self.x, self.y, LINE_THICKNESS + 10, LINE_THICKNESS + 10)
		self.health = 10

	def attack():
		pass

	def move(self, right_rect, left_rect):
		if(self.rect.right > right_rect.left):
			self.move_right = False
			self.move_left = True 
		if(self.rect.left < left_rect.right):
			self.move_left = False
			self.move_right = True
		if(self.move_left):
			self.rect.x -= 2
		elif(self.move_right):
			self.rect.x += 2
		else:
			pass
        
	def draw(self, display_surf, color):
		pygame.draw.rect(display_surf, color, self.rect)

	def draw_health(self, display_surf, color1, color2):
		health_font = pygame.font.Font('freesansbold.ttf', 10)

		health_bar_text = health_font.render('THE RED SQUARE', True, color1)
		health_bar_text_rect = health_bar_text.get_rect()
		health_bar_text_rect.topleft = (235,5)

		health_bar = pygame.Rect(235, 15, 15 * self.health, 5)
		health_bar_background = pygame.Rect(235, 15, 150, 5)

		pygame.draw.rect(display_surf, color2, health_bar_background)
		pygame.draw.rect(display_surf, color1, health_bar)
		display_surf.blit(health_bar_text, health_bar_text_rect)


		
