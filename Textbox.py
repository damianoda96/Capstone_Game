import sys
import pygame
from pygame.locals import *

class Textbox:
	def __init__(self, text, color, BASIC_FONT, y):
		self.text = BASIC_FONT.render(text, True, color)
		self.rect = self.text.get_rect()
		self.rect.topleft = (10, 15 * y)
	def draw(self, display_surf):
		display_surf.blit(self.text, self.rect)
		