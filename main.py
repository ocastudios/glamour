#!/usr/bin/env python

from getscreen import *

from pygame.locals import *
pygame.mixer.init()
import random
from sys import exit
from math import *
from random import randint
import game_clock
import obj_images
from numpy import uint8
import camera
import mousepointer
import menu
import universe
import control



#Create lists


clock = pygame.time.Clock()
universe = universe.Universe(os_screen.current_w,os_screen.current_h)

gamemenu = menu.MenuScreen(universe)



while True:
    while universe.LEVEL == 'menu':
        control.main_menu(universe)
        gamemenu.update_all()
        pygame.display.flip()
    gamemenu.speed = 0

    while universe.LEVEL == 'close':
        gamemenu.action = 'close'
        control.main_menu(universe)
        gamemenu.update_all()
        pygame.display.flip()

    while universe.LEVEL == 'choose_princess':
        control.choose_menu(universe)
        gamemenu.update_all()
        pygame.display.flip()

    while universe.LEVEL == 'close':
        gamemenu.action = 'close'
        control.main_menu(universe)
        gamemenu.update_all()
        pygame.display.flip()

    while universe.LEVEL == 'choose_princess':
        control.name_menu(universe)
        gamemenu.update_all()
        pygame.display.flip()

    universe.define_level()

    game_mouse = mousepointer.MousePointer(universe.mouse_pos,universe.level)
    gamecamera = camera.GameCamera(universe.level)

    run_level = True


    pygame.mouse.set_visible(0)

    while run_level:
        for i in universe.level.gates:
            if i.change_level:
                universe.LEVEL = i.level
                gamemenu.menu.LEVEL = i.level
                run_level = False
                i.change_level = False
                break
        control.stage(universe)
        game_mouse.update()
        time_passed = clock.tick(15)
        universe.screen_surface.fill([255,255,255])
        universe.level.update_all(universe.action,universe.dir,universe)
        universe.clock_pointer.update_image()

        pygame.display.flip()

    universe.screen_surface.fill([0,0,0])
    pygame.display.flip()

    run_level = True
