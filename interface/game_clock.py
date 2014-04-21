import utils
import pygame
import os
import settings
from settings import directory
from settings import p



class GameClock():
	def __init__(self,universe):
		self.image = utils.img.image(os.path.join(directory.interface,'clock','page_border.png'))
		self.pos =((universe.width-self.image.get_width()),0)
	def update_all(self):
		pass


class ClockPointer():
	def __init__(self,universe):
		self.universe = universe
		self.rotate_list = [float(i)/10 for i in range(-900,5,5)]
		print len(self.rotate_list)
		self.clock_pointer_basic= utils.img.image(os.path.join(directory.interface,'clock','clock_pointer.png'))
		self.count = 0
		self.tick = 0
		self.time = 'day' #morning,day,evening,night
		self.image = pygame.transform.rotate(self.clock_pointer_basic, self.rotate_list[0])
		imagesize = self.image.get_size()
		self.pos = (self.universe.width-imagesize[0],0)
		self.pointerpos = 0
		self.balltime = None

	def set_balltime(self):
		if self.universe.stage.princesses:
			princess = self.universe.stage.princesses[0]
			if (princess.points/10>120):
				extra=120
				self.pointerpos = 0
			else:
				extra=princess.points/10
				self.pointerpos = (120-extra)/2
			return 240+extra
		else:
			return None


	def update_all(self):
		self.balltime = self.balltime or self.set_balltime()
		if not self.balltime:
			self.balltime = 240
			balltime=self.balltime
			self.pointerpos = 60
		else:	
			balltime=self.balltime
		if not self.universe.level.paused:
			self.tick +=1
		if self.tick == self.universe.fps:
			if self.count < balltime:
				if self.pointerpos > (len(self.rotate_list)-2):
					self.pointerpos  =0
				else:
					if self.count%2==0:
						self.pointerpos  +=1
				if self.count < len(self.rotate_list):
					self.image = pygame.transform.rotate(self.clock_pointer_basic, self.rotate_list[self.pointerpos])#self.clock_pointer[self.count]
					imagesize = self.image.get_size()
					self.pos = (self.universe.width-imagesize[0],0)
				self.count += 1

		elif self.tick > self.universe.fps:
			self.tick = 0
		if self.count < balltime*0.15:
			self.time = 'morning'
		elif self.count < balltime*0.55:
			self.time = 'day'
		elif self.count < balltime*0.65:
			self.time = 'evening'
		elif self.count < balltime*0.8:
			self.time = 'night'
		else:
			self.time = 'ball'
