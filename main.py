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
pygame.mouse.set_visible(0)
while True:
	if universe.LEVEL == 'menu':
		control.main_menu(universe)
	elif universe.LEVEL == 'game':
		control.stage(universe)
	universe.clock.tick(universe.fps)
	universe.update_all()
	pygame.display.flip()
