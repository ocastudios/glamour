#!/usr/bin/env python
# -*- coding: utf-8 -*-

print "Starting Game"
import settings
from settings import splash
settings.welcome()
settings.splash.splash_image()
settings.initialize_mixer()
import pygame
pygame.init()

import interface.menu
import interactive.universe as universe
import interface.menu as menu
import control
import settings
import sqlite3


universe = universe.Universe()
gamemenu = menu.MenuScreen(universe)

while True:
	pygame.mouse.set_visible(0)
	while universe.LEVEL != 'start':
		control.main_menu(universe)
		universe.clock.tick(40)
		gamemenu.update_all()
		pygame.display.flip()
	universe.define_level()
	while universe.run_level:
		control.stage(universe)
		universe.clock.tick(universe.frames_per_second)
		universe.level.update_all()
		pygame.display.flip()
	universe.screen_surface.fill([0,0,0])
	pygame.display.flip()
	run_level = True
