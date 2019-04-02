import sys
import pygame
import math
import random
from pygame.locals import *
from Player import *
from Enemy import *
from Platform import *
from Controller import *

class Platform:

	def __init__(self, x, y, w, h, t):

		self.width = w
		self.height = h
		self.rect = pygame.Rect(x, y, w, h)
		self.type = t

	def move_up(self):
		pass

	def move_down(self):
		pass

	def move_left(self, vel):
		self.rect.x -= vel

	def move_right(self, vel):
		self.rect.x += vel

	def side_move(self):
		start_x = self.rect.x
		while(self.rect.x > start_x - 100):
			self.rect.x -= 3
		while(self.rect.x != start_x):
			self.rect.x += 3

	def deactivate(self):
		self.type = "inactive"


	def draw(self, display_surf, color):
		pygame.draw.rect(display_surf, color, self.rect)