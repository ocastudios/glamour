# -*- coding: utf-8 -*-
#!/usr/bin/env python

from getscreen import *

from pygame.locals import *
pygame.mixer.init()
from sys import exit
import game_clock

import obj_images
import camera
import menu
import universe
import control

try:
    import psyco
    psyco.log()
    psyco.profile(1.0)
except:
    pass

clock = pygame.time.Clock()
universe = universe.Universe(os_screen.current_w,os_screen.current_h)
del splash_surface, splash, os_screen
gamemenu = menu.MenuScreen(universe)

while True:
    while universe.LEVEL != 'start':
        while universe.LEVEL == 'menu':
            control.main_menu(universe)
            gamemenu.update_all()
            pygame.display.flip()
        while universe.LEVEL == 'close':
            gamemenu.action = 'close'
            control.main_menu(universe)
            gamemenu.update_all()
            pygame.display.flip()
    universe.define_level()
    gamecamera = camera.GameCamera(universe.level)
    pygame.mouse.set_visible(0)

    while universe.run_level:
        control.stage(universe)
        clock.tick(universe.frames_per_second)
        universe.level.update_all()
        universe.clock_pointer.update_image()
        pygame.display.flip()
        
    universe.screen_surface.fill([0,0,0])
    pygame.display.flip()
    run_level = True

