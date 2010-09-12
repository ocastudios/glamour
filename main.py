# -*- coding: utf-8 -*-
#!/usr/bin/env python
print "Starting Game"
from settings.getscreen import *
from pygame.locals import *
import interface.menu
import interactive.universe as universe
import interface.menu as menu
import control
import settings
import sqlite3

clock = pygame.time.Clock()
universe = universe.Universe()
del splash_surface, splash, os_screen
gamemenu = menu.MenuScreen(universe)

while True:
    pygame.mouse.set_visible(0)
    while universe.LEVEL != 'start':
        control.main_menu(universe)
        clock.tick(40)
        gamemenu.update_all()
        pygame.display.flip()
    universe.define_level()
    while universe.run_level:
        control.stage(universe)
        clock.tick(universe.frames_per_second)
        universe.level.update_all()
        pygame.display.flip()
    universe.screen_surface.fill([0,0,0])
    pygame.display.flip()
    run_level = True
