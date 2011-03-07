import utils
import pygame
import os
import random
from settings import directory
import settings

p = settings.p

class Drape():
	def __init__(self):
		size = p((1440,900))
		frames = []
		drapes_size = p([720,900])
		speed  = 0
		right_x	 = 0
		left_x	  = p(645)
		self.drape_images = utils.img.OneSided(directory.drapes)
		self.images = self.drape_images.list
		self.image = self.images[0]
		self.action = 'stay'
		self.speed = 0
		self.image_number = 0
		self.size = self.image.get_size()
		self.counter = 0


	def update_all(self):
		self.counter += 1
		if self.counter >5:
			if self.action == "open" and self.image_number < len(self.images)-1:
				self.image_number +=1
			elif self.action =="close" and self.image_number > -len(self.images):
				self.image_number -=1
			self.image = self.images[self.image_number]
	def __del__(self):
		print "Drape destroyed"

class UperDrape():
	def __init__(self):
		self.image = utils.img.image(os.path.join(directory.upper_drapes,'upper.png'))
		self.action = 'stay'
		self.y = 0
		self.size_y = p(356)

	def update_all(self):
		if self.action == 'open':
			self.y -= p(3)
		if self.y < -self.size_y:
			self.y = -self.size_y
