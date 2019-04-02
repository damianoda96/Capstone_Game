import sys
import pygame
import math
import random
from pygame.locals import *
from Player import *
from Enemy import *
from Platform import *
from Controller import *

class Bullet:

	def __init__(self, x, y, dest_x, dest_y, LINE_THICKNESS):
	
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


	def draw(self, display_surf):
		pygame.draw.rect(display_surf, WHITE, self.rect)