# -*- coding: utf-8 -*-
import pygame
import interactive.stage as stage
import os
import interface.menu as menu
import interface.mousepointer as mousepointer
from settings import *
import check
import inspect
import utils

class Universe():
	def __init__(self):
		default_resolution = (1440,900)
		w = int(round(default_resolution[0]*scale))
		h = int(round(default_resolution[1]*scale))
		self.clock = pygame.time.Clock()
		self.main_dir = main_dir
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
		self.screen_surface = pygame.display.set_mode((w,h),32)#,pygame.FULLSCREEN , 32)
		self.screen_surface.blit(utils.img.image(os.path.join(directory.drapes,"drape000.png")),(0,0))
		self.screen_surface.blit(utils.img.image(os.path.join(directory.upper_drapes,"upper.png")),(0,0))
		pygame.display.flip()
		## Interface ##
		self.pointer	 = mousepointer.MousePointer(self,type = 2)
		self.level = menu.Menu(self)
		self.level.main()



	def update_all(self):
		self.pointer.update()
		self.level.update_all()

		if (self.LEVEL == 'menu' and self.level.__class__ != menu.Menu) or (self.LEVEL == 'game' and self.level.__class__ != stage.Stage):
			self.define_level()


	def define_level(self):
		if self.LEVEL == 'game':
			if not self.level or self.level.__class__ != stage.Stage:
				self.fts = 20
				self.action = [None,'stay',None]
				self.del_all(self.level)
				self.pointer	 = mousepointer.MousePointer(self)
				self.level = stage.Stage(self)
				self.level.BathhouseSt()
		elif self.LEVEL == 'menu':
			if not self.level or self.level.__class__ != menu.Menu:
				self.fps = 40
				self.action = ['open','stay','open']
				self.del_all(self.level)
				self.pointer	 = mousepointer.MousePointer(self,type = 2)
				self.level = menu.Menu(self)
				self.level.main()

	def del_all(self, victim):
		def del_list(victim_list):
			for i in victim_list:
				del i
			del victim_list
		if victim.__class__ == stage.Stage:
			del victim.name
			del victim.size
			del_list(victim.cameras)
			del_list(victim.gates)
			del_list(victim.clock)
			del_list(victim.floor_heights)
			del victim.floor
			del_list(victim.menus)
			del_list(victim.panel)
			del_list(victim.pointer)
			del_list(victim.scenarios_front)
			del_list(victim.animated_scenarios)
			del_list(victim.blitlist)
			del_list(victim.foreground)
			del victim.white
			del victim.black
			del victim.bar
			del victim.bar_goal
			del victim.bar_speed
			del_list(victim.pointer)
			del victim.inside
			del victim.princess_castle
			del victim.fairy
			del victim.omni_directory
			del victim.ball
			del victim.ballroom
			del victim.event_counter
			del victim.starting_game
			del_list( victim.fae)
			del victim.pause
			del victim.paused
			del victim.water_level
			del victim.exit_sign
			del_list( victim.loading_icons)
			del victim.margin
			del victim.enemy_channel
			del victim.unlocking
		elif victim.__class__ == menu.Menu:
			del victim.vertical_bar
			del victim.speed
			del victim.goal_pos
			del victim.position
			del victim.background
			del victim.size
			del victim.action
			del victim.next_menu
			del victim.print_princess
			del victim.princess
			del victim.story
			del victim.tutorial
			del victim.credits
			del victim.go_back
			del victim.back_background
			del victim.mouse_positions
			del victim.selector
			del victim.hoover_letter
			del victim.hoover_letter_size
			del victim.hoover_large
			del victim.hoover_large_size
			del victim.STEP
			del_list(victim.story_frames)
			del victim.drapes
			del victim.upper_drapes
			del victim.count

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
