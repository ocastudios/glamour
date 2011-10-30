import utils
import pygame
import os
import settings
from settings import directory
from settings import p



class GameClock():
	def __init__(self,universe):
		self.image = utils.img.image(os.path.join(directory.interface,'clock','page_border.png'))
		self.pos   =((universe.width-self.image.get_width()),0)
	def update_all(self):
		pass


class ClockPointer():
	def __init__(self,universe):
		self.universe		  = universe
		self.rotate_list	= [float(i)/10 for i in range(-900,5,5)]
		self.clock_pointer_basic= utils.img.image(os.path.join(directory.interface,'clock','clock_pointer.png'))
		self.clock_pointer	  = []
		self.count			  = 0
		self.tick			   = 0
		self.time			   = 'day' #morning,day,evening,night
		self.clock_pointer = [pygame.transform.rotate(self.clock_pointer_basic,degree) for degree in self.rotate_list]
		self.image  = self.clock_pointer[self.count]
		imagesize   = self.image.get_size()
		self.pos	= (self.universe.width-imagesize[0],0)
		self.pointerpos = 0
		

	def update_all(self):
		if not self.universe.level.paused:
			self.tick +=1
		if self.tick == self.universe.fps:
			if self.count %100 == 0:
				print "Updating the time "+ str(self.count)
				print "Music volume " +str(pygame.mixer.music.get_volume())
			if self.count < 180:
				if self.pointerpos > (len(self.rotate_list)-2):
					self.pointerpos  =0
				else:
					self.pointerpos  +=1
				self.image  = self.clock_pointer[self.count]
				imagesize   = self.image.get_size()
				self.pos	= (self.universe.width-imagesize[0],0)
				self.count += 1

		elif self.tick > self.universe.fps:
			self.tick = 0
		if self.count < 40:
			self.time = 'morning'
		elif self.count < 80:
			self.time = 'day'
		elif self.count < 120:
			self.time = 'evening'
		elif self.count < 179:
			self.time = 'night'
		else:
			self.time = 'ball'


