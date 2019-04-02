import sys
import pygame
import math
import random
from pygame.locals import *
from Player import *
from Enemy import *
from Platform import *
from Controller import *

# Enemy Class

class Enemy:

	def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, LINE_THICKNESS):

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

	def draw(self, display_surf):

		pygame.draw.rect(display_surf, blue, self.rect)