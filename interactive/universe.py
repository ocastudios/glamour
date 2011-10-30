# -*- coding: utf-8 -*-
import pygame
import os
import interface.menu as menu
import interface.mousepointer as mousepointer
from settings import *
import inspect
import utils
from settings import directory

class Universe():
	def __init__(self):
		default_resolution = (1440,900)
		w = int(round(default_resolution[0]*scale))
		h = int(round(default_resolution[1]*scale))
		self.clock = pygame.time.Clock()
		self.center_x = int(-3400*scale)
		self.center_y = 0
		self.floor = self.height = h
		self.width = w
		self.speed = 0
		self.LEVEL = 'menu'
		self.action = [None,'stay','open']
		self.dir	= 'right'
		self.click = False
		self.file = None
		self.fps = 40 #fps is altered by stage and menu in their initialization
		self.run_level = True
		self.db = None
		self.db_cursor = None
### Uncomment next line (and comment the following) to test the game with different resolutions
### you will also need to edit the setting.__init__ file.
#		self.screen_surface = pygame.display.set_mode((w,h),32)
		self.screen_surface = pygame.display.set_mode((w,h),pygame.FULLSCREEN , 32)
		self.screen_surface.blit(utils.img.image(os.path.join(directory.drapes,"drape000.png")),(0,0))
		self.screen_surface.blit(utils.img.image(os.path.join(directory.upper_drapes,"upper.png")),(0,0))
		pygame.display.flip()
		## Interface ##
		self.pointer	 = mousepointer.MousePointer(self,type = 2)
		self.menu = menu.Menu(self)
		self.stage = None
		self.level = self.menu
		self.level.main()



	def update_all(self):
		self.pointer.update()
		self.level.update_all()
		if self.LEVEL == 'menu' and self.level.__class__ != menu.Menu:
			self.define_level()
		if self.LEVEL == 'game':
			try:
				stage
			except:
				global stage
				import interactive.stage as stage
			if self.level.__class__ != stage.Stage:
				self.define_level()


	def define_level(self):
		if self.LEVEL == 'game':
			if not self.level or self.level.__class__ != stage.Stage:
				self.fps = 20
				self.action = [None,'stay',None]
#				self.del_all(self.level)
				self.pointer.images	 = self.pointer.images_big
				self.stage = self.stage or stage.Stage(self)
				self.level = self.stage
				self.level.paused = False
				self.stage.BathhouseSt(goalpos = round(5220*scale))
				
		elif self.LEVEL == 'menu':
			if not self.level or self.level.__class__ != menu.Menu:
				self.fps = 40
				self.action = ['open','stay','open']
#				self.del_all(self.level)
				self.pointer.images	 = self.pointer.images_small
				self.level = self.menu
				self.level.vertical_bar['side'] = 'left'
				self.level.main()

	def movement(self,dir):
		max_speed = round(14*scale)
		if self.speed > max_speed:
			self.speed = max_speed
		elif self.speed< -max_speed:
			self.speed = -max_speed
		self.center_x += self.speed
		if self.center_x > 0:
			self.speed = 0
			self.center_x = 0
		if self.center_x - self.width < -(self.level.size):
			self.speed = 0
			self.center_x = -(self.level.size) + self.width
