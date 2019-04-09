import sys
import pygame
import math
import random
from pygame.locals import *
from Player import *
from Enemy import *
from Platform import *
from Controller import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
LINE_THICKNESS = 10
red = pygame.Color('firebrick1')

# Enemy Class

class Enemy:

	def __init__(self):

		self.type = "blah" # eventually for random enemies

		self.x = WINDOW_WIDTH
		self.y = WINDOW_HEIGHT

		self.rect = pygame.Rect(self.x, self.y, LINE_THICKNESS, LINE_THICKNESS)

	def move(self, dest_x, dest_y):

		if self.rect.x < dest_x:
			self.rect.x += 2
		if self.rect.x > dest_x:
			self.rect.x -= 2

		if self.rect.y > dest_y:
			self.rect.y -= 2
		if self.rect.y < dest_y:
			self.rect.y += 2

	def draw(self, display_surf):

		pygame.draw.rect(display_surf, red, self.rect)